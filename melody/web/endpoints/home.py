from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.responses import HTMLResponse

from melody.kit.core import app
from melody.web.core import environment
from melody.web.dependencies import optional_cookie_token_dependency

__all__ = ("get_home",)

PAGE_TEMPLATE = environment.get_template("page.html")


@app.get("/")
async def get_home(
    user_id: Optional[UUID] = Depends(optional_cookie_token_dependency)
) -> HTMLResponse:
    if user_id is None:
        return HTMLResponse(await PAGE_TEMPLATE.render_async())

    return HTMLResponse()
