from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from melody.kit.constants import NAME, V1, VERSION_1
from melody.kit.database import Database
from melody.kit.errors import AnyError, Error

__all__ = ("database", "app", "v1")

database = Database()

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
