from fastapi import status
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from melody.kit.core import app
from melody.kit.errors import AnyError, Error, ErrorCode, InternalError
from melody.web.constants import BREAK, NEW_LINE, STATIC, STATIC_NAME, STATIC_PATH, TEMPLATES

__all__ = ("environment",)

environment = Environment(
    loader=FileSystemLoader(TEMPLATES),
    trim_blocks=True,
    lstrip_blocks=True,
    enable_async=True,
)

ERROR_TEMPLATE = environment.get_template("error.html")

app.mount(STATIC_PATH, StaticFiles(directory=STATIC), name=STATIC_NAME)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Error)  # type: ignore
    async def error_handler(request: Request, error: AnyError) -> HTMLResponse:
        return HTMLResponse(
            await ERROR_TEMPLATE.render_async(detail=error.detail, code=error.code.value),
            status_code=error.status_code,
        )

    @app.exception_handler(RequestValidationError)  # type: ignore
    async def validation_error_handler(request: Request, error: RequestValidationError) -> HTMLResponse:
        converted_error = Error(
            str(error).replace(NEW_LINE, BREAK),
            code=ErrorCode.UNPROCESSABLE_ENTITY,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

        return await error_handler(request, converted_error)  # type: ignore

    @app.exception_handler(Exception)  # type: ignore
    async def internal_error_handler(request: Request, error: Exception) -> HTMLResponse:
        internal_error = InternalError()

        return await error_handler(request, internal_error)  # type: ignore


register_error_handlers(app)
