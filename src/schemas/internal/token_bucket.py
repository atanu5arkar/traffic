import time
from dataclasses import dataclass


@dataclass
class TokenBucket:
    size: int
    rps: int
    tokens: int
    last_used: float = time.time()


@dataclass
class ClientState:
    limit: str
    remaining: str
    reset: str
