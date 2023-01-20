from typing import Dict
from uuid import UUID

from argon2 import PasswordHasher
from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pendulum import DateTime

from melody.kit.config import get_config
from melody.kit.constants import NAME, V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import AnyError, Error

__all__ = ("config", "database", "hasher", "tokens", "app", "v1")

database = Database()

config = get_config()

hasher = PasswordHasher(
    time_cost=config.hash.time_cost,
    memory_cost=config.hash.memory_cost,
    parallelism=config.hash.parallelism,
)

tokens: Dict[UUID, DateTime] = {}

app = FastAPI(openapi_url=None, redoc_url=None)


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(Error)  # type: ignore
    async def error_handler(request: Request, error: AnyError) -> JSONResponse:  # type: ignore
        return JSONResponse(
            status_code=error.status_code,
            content=error.into_data(),
        )


v1 = FastAPI(title=NAME, version=VERSION_1)

app.mount(V1, v1)

register_error_handler(app)
register_error_handler(v1)
