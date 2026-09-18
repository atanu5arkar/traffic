from pydantic import BaseModel, Field


# Is there any possible constraint between these attributes?
class SetLimit(BaseModel):
    rps: int = Field(gt=0)
    burst_size: int = Field(gt=0, lt=100)
