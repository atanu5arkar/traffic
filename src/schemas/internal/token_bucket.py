import time
from dataclasses import dataclass


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
