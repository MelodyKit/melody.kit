from typing import Optional, Union
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse

from melody.kit.core import app
from melody.kit.endpoints.authentication import login as kit_login
from melody.kit.endpoints.authentication import logout as kit_logout
from melody.kit.endpoints.authentication import register as kit_register
from melody.kit.endpoints.authentication import verify as kit_verify
from melody.web.constants import TOKEN
from melody.web.core import environment
from melody.web.dependencies import cookie_token_dependency

__all__ = ("login", "logout", "register", "verify")

LOGIN_TEMPLATE = environment.get_template("login.html")


@app.get("/login", response_model=None)
async def login(
    email: Optional[str] = None, password: Optional[str] = None
) -> Union[HTMLResponse, RedirectResponse]:
    if email is not None and password is not None:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

        token_data = await kit_login(email, password)

        token = token_data[TOKEN]

        response.set_cookie(TOKEN, token)

        return response

    return HTMLResponse(await LOGIN_TEMPLATE.render_async())


@app.get("/logout")
async def logout(user_id: UUID = Depends(cookie_token_dependency)) -> RedirectResponse:
    await kit_logout(user_id)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    response.delete_cookie(TOKEN)

    return response


REGISTER_TEMPLATE = environment.get_template("register.html")


@app.get("/register", response_model=None)
async def register(
    name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None
) -> Union[HTMLResponse, RedirectResponse]:
    if name is not None and email is not None and password is not None:
        await kit_register(name, email, password)

        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    return HTMLResponse(await REGISTER_TEMPLATE.render_async())


@app.get("/verify/{user_id}/{verification_token}")
async def verify(user_id: UUID, verification_token: str) -> RedirectResponse:
    await kit_verify(user_id, verification_token)

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
