from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app

__all__ = ("redirect_docs",)

DOCS = "https://melodykit.github.io/"


@app.get("/docs/{name}")
async def redirect_docs(name: str) -> RedirectResponse:
    return RedirectResponse(DOCS + name, status_code=status.HTTP_302_FOUND)
