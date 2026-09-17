from typing import Annotated

from fastapi import FastAPI, Header

from src.services.rate_limiter_service import service

app = FastAPI(title="Traffic", root_path="/limit")


@app.get("/")
def handle_req_limit(x_client_key: Annotated[str, Header()]):
    return service.limiter(x_client_key)


@app.post("/set")
def handle_set_limit(x_client_key: Annotated[str, Header()]):
    return service.set_limit(x_client_key)
