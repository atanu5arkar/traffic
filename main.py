import math
import time
from dataclasses import dataclass


@dataclass
class TokenBucket:
    size: int = 10
    rps: int = 1
    tokens: int = size
    last_used: float = time.time()

store = {}


def fill(bucket: TokenBucket):
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


def check_bucket(key):
    bucket = store.get(key)

    if not bucket:
        bucket = TokenBucket()
        store[key] = bucket
        bucket.tokens -= 1
        return True

    fill(bucket)
    if bucket.tokens == 0:
        return False

    bucket.tokens -= 1
    return True


def limiter(req):
    # Part of req headers
    key = "1"
    result = check_bucket(key)
    # Return a proper rate-limit response with 429 status
    return "ALLOW" if result else "DENY"


if __name__ == "__main__":
    for i in range(1, 13):
        res = limiter({})
        print(f"req{i}: {res}")
