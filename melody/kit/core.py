from argon2 import PasswordHasher
from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from melody.kit.config import get_config
from melody.kit.constants import V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import AnyError, Error, InternalError
from melody.kit.typing import UUIDDict
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS

__all__ = ("config", "database", "redis", "hasher", "app", "v1")

database = Database()

config = get_config()

redis = Redis(  # type: ignore
    host=config.redis.host,
    port=config.redis.port,
    encoding=DEFAULT_ENCODING,
    encoding_errors=DEFAULT_ERRORS,
    decode_responses=True,
)

hasher = PasswordHasher(
    time_cost=config.hash.time_cost,
    memory_cost=config.hash.memory_cost,
    parallelism=config.hash.parallelism,
)

verification_tokens: UUIDDict[str] = {}

app = FastAPI(openapi_url=None, redoc_url=None)

INTERNAL_SERVER_ERROR = "internal server error"

ORIGIN = f"{config.open}.{config.domain}"


def register_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


register_cors_middleware(app)


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
