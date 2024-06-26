from typing import Any, Dict

from argon2 import PasswordHasher
from authlib.integrations.starlette_client import OAuth  # type: ignore[import-untyped]
from fastapi import status
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from starlette.exceptions import HTTPException as HTTPError
from starlette.middleware.sessions import SessionMiddleware  # XXX: use `fastapi` when implemented
from typing_aliases import NormalError, StringDict

from melody.kit.config.core import CONFIG
from melody.kit.config.keyring import KEYRING
from melody.kit.constants import V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors.core import Error, ErrorData
from melody.kit.errors.internal import InternalError
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, STAR
from melody.shared.typing import IntString

__all__ = ("config", "database", "redis", "hasher", "oauth", "app", "v1")

database = Database()
"""The database instance to use."""

config = CONFIG
"""The config instance to use."""

keyring = KEYRING
"""The keyring instance to use."""

redis = Redis(
    host=config.redis.host,
    port=config.redis.port,
    encoding=DEFAULT_ENCODING,
    encoding_errors=DEFAULT_ERRORS,
    decode_responses=True,
)
"""The redis instance to use."""

hasher = PasswordHasher(
    time_cost=config.hash.time_cost,
    memory_cost=config.hash.memory_cost,
    parallelism=config.hash.parallelism,
)
"""The hasher instance to use."""

oauth = OAuth()
"""The oauth instance to use."""

DISCORD = "discord"
DISCORD_AUTHORIZE_URL = "https://discord.com/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_SCOPE = "identify"

oauth.register(
    DISCORD,
    authorize_url=DISCORD_AUTHORIZE_URL,
    access_token_url=DISCORD_TOKEN_URL,
    scope=DISCORD_SCOPE,
    client_id=keyring.discord.id,
    client_secret=keyring.discord.secret,
)

SPOTIFY = "spotify"
SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SCOPE = ""  # TODO

oauth.register(
    SPOTIFY,
    authorize_url=SPOTIFY_AUTHORIZE_URL,
    access_token_url=SPOTIFY_TOKEN_URL,
    scope=SPOTIFY_SCOPE,
    client_id=keyring.spotify.id,
    client_secret=keyring.spotify.secret,
)

app = FastAPI(openapi_url=None, redoc_url=None)
"""The main application."""

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
    app.add_middleware(SessionMiddleware, secret_key=keyring.session)


register_cors_middleware(app)
register_session_middleware(app)


UNHANDLED_ERROR = "unhandled error"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Error)
    async def error_handler(request: Request, error: Error) -> JSONResponse:
        return JSONResponse(error.into_data(), status_code=error.status_code)

    @app.exception_handler(HTTPError)
    async def http_error_handler(request: Request, error: HTTPError) -> JSONResponse:
        converted_error = Error.from_http_error(error)

        return await error_handler(request, converted_error)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, error: RequestValidationError
    ) -> JSONResponse:
        converted_error = Error.from_validation_error(error)

        return await error_handler(request, converted_error)

    @app.exception_handler(NormalError)
    async def normal_error_handler(request: Request, error: NormalError) -> JSONResponse:
        internal_error = InternalError()

        return await error_handler(request, internal_error)


VALIDATION_ERROR = "Validation error"

OVERRIDE_VALIDATION_ERROR: Dict[IntString, StringDict[Any]] = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: dict(description=VALIDATION_ERROR, model=ErrorData),
}

v1 = FastAPI(title=config.name, version=VERSION_1, responses=OVERRIDE_VALIDATION_ERROR)
"""The `/v1` application."""

app.mount(V1, v1)

register_error_handlers(v1)
