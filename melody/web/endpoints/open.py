from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app, config

__all__ = ("redirect_open",)

OPEN = "https://{config.open}.{config.domain}/"

open = OPEN.format


@app.get("/open")
async def redirect_open() -> RedirectResponse:
    return RedirectResponse(open(config=config), status_code=status.HTTP_302_FOUND)
