from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app

__all__ = ("redirect_github",)

GITHUB = "https://github.com/MelodyKit/"


@app.get("/github/{name}")
async def redirect_github(name: str) -> RedirectResponse:
    return RedirectResponse(GITHUB + name, status_code=status.HTTP_302_FOUND)
