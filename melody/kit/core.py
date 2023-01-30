from typing import Dict
from uuid import UUID

from argon2 import PasswordHasher
from fastapi import status
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pendulum import DateTime

from melody.kit.config import get_config
from melody.kit.constants import V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import AnyError, Error, InternalError

__all__ = ("config", "database", "hasher", "tokens", "app", "v1")

database = Database()

config = get_config()

hasher = PasswordHasher(
    time_cost=config.hash.time_cost,
    memory_cost=config.hash.memory_cost,
    parallelism=config.hash.parallelism,
)

tokens: Dict[UUID, DateTime] = {}
verification_tokens: Dict[UUID, str] = {}

app = FastAPI(openapi_url=None, redoc_url=None)

INTERNAL_SERVER_ERROR = "internal server error"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Error)  # type: ignore
    async def error_handler(request: Request, error: AnyError) -> JSONResponse:
        return JSONResponse(error.into_data(), status_code=error.status_code)

    @app.exception_handler(Exception)  # type: ignore
    async def internal_error_handler(request: Request, error: Exception) -> JSONResponse:
        internal_error = InternalError()

        return await error_handler(request, internal_error)  # type: ignore


v1 = FastAPI(title=config.name, version=VERSION_1)

app.mount(V1, v1)

register_error_handlers(v1)
