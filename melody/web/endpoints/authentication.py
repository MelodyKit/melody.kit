from uuid import UUID

from fastapi import Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from melody.kit.core import app
from melody.kit.endpoints.authentication import login as kit_login
from melody.kit.endpoints.authentication import logout as kit_logout
from melody.kit.endpoints.authentication import register as kit_register
from melody.kit.endpoints.authentication import verify as kit_verify
from melody.web.constants import TOKEN
from melody.web.core import environment
from melody.web.dependencies import (
    cookie_token_dependency, form_email_deliverability_dependency, form_email_dependency
)

__all__ = ("get_login", "login", "logout", "get_register", "register", "verify")

LOGIN_TEMPLATE = environment.get_template("login.html")


@app.get("/login")
async def get_login() -> HTMLResponse:
    return HTMLResponse(await LOGIN_TEMPLATE.render_async())


@app.post("/login")
async def login(
    email: str = Depends(form_email_dependency), password: str = Form()
) -> RedirectResponse:
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    token_data = await kit_login(email, password)

    token = token_data[TOKEN]

    response.set_cookie(TOKEN, token)

    return response


@app.get("/logout")
async def logout(user_id: UUID = Depends(cookie_token_dependency)) -> RedirectResponse:
    await kit_logout(user_id)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    response.delete_cookie(TOKEN)

    return response


REGISTER_TEMPLATE = environment.get_template("register.html")


@app.get("/register")
async def get_register() -> HTMLResponse:
    return HTMLResponse(await REGISTER_TEMPLATE.render_async())


@app.post("/register")
async def register(
    name: str = Form(),
    email: str = Depends(form_email_deliverability_dependency),
    password: str = Form(),
) -> RedirectResponse:
    await kit_register(name, email, password)

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


@app.get("/verify/{user_id}/{verification_token}")
async def verify(user_id: UUID, verification_token: str) -> RedirectResponse:
    await kit_verify(user_id, verification_token)

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
