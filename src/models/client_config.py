from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ClientConfig(BaseModel):
    key: str
    rps: int
    burst_size: int
    created_at: datetime = Field(default=datetime.now(timezone.utc))


class ShortClientConfig(BaseModel):
    rps: int
    burst_size: int
