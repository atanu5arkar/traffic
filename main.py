from typing import Annotated

from fastapi import FastAPI, Header

from src.services.rate_limiter_service import service

app = FastAPI(title="Traffic")


@app.get("/limit")
def handle_req_limit(x_client_key: Annotated[str, Header()]):
    return service.limiter(x_client_key)
