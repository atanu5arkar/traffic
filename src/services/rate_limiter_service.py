import math
import time

from fastapi.responses import JSONResponse

from src.constants import DEFAULT_BUCKET
from src.repositories.config_repository import config_repo
from src.schemas.internal.token_bucket import ClientState, TokenBucket


class RateLimiterService:
    def __init__(self) -> None:
        self._store = {}

    def limiter(self, key: str):
        msg, state = self._check_bucket(key)
        return JSONResponse(
            content={"msg": msg},
            status_code=200 if msg == "ALLOW" else 429,
            headers={
                "x-ratelimit-limit": state.limit,
                "x-ratelimit-remaining": state.remaining,
                "x-ratelimit-reset": state.reset,
            },
        )

    def set_limit(self, key: str):
        config_repo.add(key)
        return JSONResponse(content={"msg": "Created"}, status_code=201)

    def _check_bucket(self, key: str) -> tuple[str, ClientState]:
        msg = ""
        bucket: TokenBucket | None = self._store.get(key)

        # Handle the first request from the client
        if not bucket:
            bucket = self._create_bucket(key)
            self._store[key] = bucket

        # Compensate for the elapsed time before deducting more tokens
        self._refill(bucket)

        if bucket.tokens == 0:
            msg = "DENY"
        else:
            msg = "ALLOW"
            bucket.tokens -= 1
            bucket.last_used = time.time()

        state = self._client_state(bucket)
        return msg, state

    def _create_bucket(self, key: str):
        # Can use custom limits for the client, if available
        conf = config_repo.get(key)
        attributes = (
            {"size": conf.burst_size, "rps": conf.rps, "tokens": conf.burst_size}
            if conf
            else DEFAULT_BUCKET
        )
        return TokenBucket(**attributes)

    def _client_state(self, bucket: TokenBucket):
        limit = bucket.size
        remaining = bucket.tokens
        reset_time = int(time.time() + (limit - remaining) * bucket.rps)
        return ClientState(
            limit=str(limit), remaining=str(remaining), reset=str(reset_time)
        )

    def _refill(self, bucket: TokenBucket):
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


service = RateLimiterService()
