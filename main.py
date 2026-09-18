from typing import Annotated

from fastapi import FastAPI, Header

from src.schemas.requests.set_limit import SetLimit
from src.services.rate_limiter_service import service

app = FastAPI(title="Traffic", root_path="/limit")

StrHeader = Annotated[str, Header()]


@app.get("/")
async def handle_req_limit(x_client_key: StrHeader):
    return await service.limiter(x_client_key)


@app.post("/set")
async def handle_set_limit(x_client_key: StrHeader, body: SetLimit):
    return await service.set_limit(x_client_key, body)
