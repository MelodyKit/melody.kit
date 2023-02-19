from typing import Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import RedirectResponse

from melody.kit.core import app, config
from melody.web.dependencies import optional_cookie_token_dependency

__all__ = ("redirect_open",)

OPEN = "https://{config.open}.{config.domain}/"

open = OPEN.format


@app.get(f"/{config.open}")
async def redirect_open(
    user_id: Optional[UUID] = Depends(optional_cookie_token_dependency)
) -> RedirectResponse:
    if user_id is None:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    return RedirectResponse(open(config=config), status_code=status.HTTP_302_FOUND)
