from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app

__all__ = ("redirect_docs",)

DOCS = "https://docs.melodykit.app/"


@app.get("/docs")
async def redirect_docs() -> RedirectResponse:
    return RedirectResponse(DOCS, status_code=status.HTTP_302_FOUND)
