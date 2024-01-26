from argon2 import PasswordHasher
from authlib.integrations.starlette_client import OAuth  # type: ignore[import-untyped]
from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from starlette.middleware.sessions import SessionMiddleware  # XXX: use `fastapi` when implemented
from typing_aliases import NormalError

from melody.kit.config import CONFIG
from melody.kit.constants import V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import UNHANDLED_ERROR, Error, InternalError
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, STAR

__all__ = ("config", "database", "redis", "hasher", "oauth", "app", "v1")

database = Database()

config = CONFIG

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

oauth = OAuth()

DISCORD = "discord"
DISCORD_AUTHORIZE_URL = "https://discord.com/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_SCOPE = "identify"

oauth.register(
    DISCORD,
    authorize_url=DISCORD_AUTHORIZE_URL,
    access_token_url=DISCORD_TOKEN_URL,
    scope=DISCORD_SCOPE,
    client_id=config.discord.client_id,
    client_secret=config.discord.client_secret,
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
        allow_methods=[STAR],
        allow_headers=[STAR],
    )


def register_session_middleware(app: FastAPI) -> None:
    app.add_middleware(SessionMiddleware, secret_key=config.session_key)


register_cors_middleware(app)
register_session_middleware(app)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Error)
    async def error_handler(request: Request, error: Error) -> JSONResponse:
        return JSONResponse(error.into_data(), status_code=error.STATUS_CODE)

    @app.exception_handler(NormalError)
    async def internal_error_handler(request: Request, error: NormalError) -> JSONResponse:
        internal_error = InternalError(UNHANDLED_ERROR)

        return await error_handler(request, internal_error)


AUTHORIZE = "/authorize"
TOKEN = "/token"
REFRESH = "/refresh"

v1 = FastAPI(title=config.name, version=VERSION_1)

app.mount(V1, v1)

register_error_handlers(v1)
