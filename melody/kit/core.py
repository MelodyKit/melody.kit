from argon2 import PasswordHasher
from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from typing_aliases import NormalError

from melody.kit.config import get_config
from melody.kit.constants import V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import Error, InternalError
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS

__all__ = ("config", "database", "redis", "hasher", "app", "v1")

database = Database()

config = get_config()

redis = Redis(
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

app = FastAPI(openapi_url=None, redoc_url=None)

ORIGIN = f"https://{config.open}.{config.domain}"

LOCAL_ORIGIN = f"http://{config.web.host}:{config.web.port}"

TAURI_ORIGIN = "tauri://localhost"
OTHER_TAURI_ORIGIN = "https://tauri.localhost"


def register_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[ORIGIN, LOCAL_ORIGIN, TAURI_ORIGIN, OTHER_TAURI_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


register_cors_middleware(app)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Error)
    async def error_handler(request: Request, error: Error) -> JSONResponse:
        return JSONResponse(error.into_data(), status_code=error.status_code)

    @app.exception_handler(NormalError)
    async def internal_error_handler(request: Request, error: NormalError) -> JSONResponse:
        internal_error = InternalError()

        return await error_handler(request, internal_error)


v1 = FastAPI(title=config.name, version=VERSION_1)

app.mount(V1, v1)

register_error_handlers(v1)
