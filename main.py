import math
import time
from dataclasses import dataclass
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse


@dataclass
class TokenBucket:
    size: int = 10
    rps: int = 1
    tokens: int = size
    last_used: float = time.time()


@dataclass
class ClientState:
    limit: str
    remaining: str
    reset: str


store = {}
app = FastAPI(title="Traffic")


def refill(bucket: TokenBucket):
    now = time.time()
    time_elapsed: int = math.floor(now - bucket.last_used)
    if not time_elapsed:
        return

    tokens_to_add = bucket.rps * time_elapsed
    new_tokens = bucket.tokens + tokens_to_add

    if new_tokens > bucket.size:
        bucket.tokens = bucket.size
    else:
        bucket.tokens = new_tokens
    return


def get_client_state(bucket: TokenBucket):
    limit = bucket.size
    remaining = bucket.tokens
    reset_time = int(time.time() + (limit - remaining) * bucket.rps)
    return ClientState(
        limit=str(limit), remaining=str(remaining), reset=str(reset_time)
    )


def check_bucket(key: str) -> tuple[str, ClientState]:
    bucket: TokenBucket | None = store.get(key)

    # Handle the first request from the client
    if not bucket:
        bucket = TokenBucket()
        bucket.tokens -= 1
        store[key] = bucket
        return "ALLOW", get_client_state(bucket)

    refill(bucket)
    state = get_client_state(bucket)

    if bucket.tokens == 0:
        return "DENY", state

    bucket.tokens -= 1
    bucket.last_used = time.time()
    return "ALLOW", state


def limiter(key: str):
    msg, state = check_bucket(key)
    return JSONResponse(
        content={"message": msg},
        status_code=200 if msg == "ALLOW" else 429,
        headers={
            "x-ratelimit-limit": state.limit,
            "x-ratelimit-remaining": state.remaining,
            "x-ratelimit-reset": state.reset,
        },
    )


@app.get("/limit")
def handle_limit(x_client_key: Annotated[str, Header()]):
    return limiter(x_client_key)
