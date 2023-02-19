from uuid import UUID

from fastapi import Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from melody.kit.core import app, config
from melody.kit.dependencies import BoundToken
from melody.kit.endpoints.authentication import forgot as kit_forgot
from melody.kit.endpoints.authentication import login as kit_login
from melody.kit.endpoints.authentication import logout as kit_logout
from melody.kit.endpoints.authentication import register as kit_register
from melody.kit.endpoints.authentication import reset as kit_reset
from melody.kit.endpoints.authentication import revoke as kit_revoke
from melody.kit.endpoints.authentication import verify as kit_verify
from melody.kit.errors import Unauthorized
from melody.kit.tokens import Token
from melody.shared.constants import TOKEN
from melody.web.core import environment
from melody.web.dependencies import (
    bound_cookie_token_dependency,
    cookie_token_dependency,
    form_email_deliverability_dependency,
    form_email_dependency,
)

__all__ = (
    "get_login",
    "login",
    "logout",
    "revoke",
    "get_register",
    "register",
    "verify",
    "get_reset",
    "reset",
)

LOGIN_TEMPLATE = environment.get_template("login.html")


@app.get("/login")
async def get_login() -> HTMLResponse:
    return HTMLResponse(await LOGIN_TEMPLATE.render_async())


@app.post("/login")
async def login(
    email: str = Depends(form_email_dependency), password: str = Form()
) -> RedirectResponse:
    response = RedirectResponse(f"/{config.open}", status_code=status.HTTP_302_FOUND)

    token_data = await kit_login(email, password)

    token = Token.from_data(token_data)

    expires_at = token.expires_at

    expires = None if expires_at is None else expires_at.int_timestamp

    response.set_cookie(TOKEN, token.token, expires=expires)

    return response


@app.get("/logout")
async def logout(
    bound_token: BoundToken = Depends(bound_cookie_token_dependency),
) -> RedirectResponse:
    await kit_logout(bound_token)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    response.delete_cookie(TOKEN)

    return response


@app.get("/revoke")
async def revoke(user_id: UUID = Depends(cookie_token_dependency)) -> RedirectResponse:
    await kit_revoke(user_id)

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

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


FORGOT_TEMPLATE = environment.get_template("forgot.html")


@app.get("/forgot")
async def get_forgot() -> HTMLResponse:
    return HTMLResponse(await FORGOT_TEMPLATE.render_async())


@app.post("/forgot")
async def forgot(email: str = Depends(form_email_dependency)) -> RedirectResponse:
    await kit_forgot(email)

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


RESET_TEMPLATE = environment.get_template("reset.html")


@app.get("/reset")
async def get_reset(
    bound_token: BoundToken = Depends(bound_cookie_token_dependency),
) -> HTMLResponse:
    response = HTMLResponse(await RESET_TEMPLATE.render_async())

    response.set_cookie(TOKEN, bound_token.token)

    return response


PASSWORD_MISMATCH = "password mismatch"


@app.post("/reset")
async def reset(
    user_id: UUID = Depends(cookie_token_dependency),
    password: str = Form(),
    confirm_password: str = Form(),
) -> RedirectResponse:
    if password != confirm_password:
        raise Unauthorized(PASSWORD_MISMATCH)

    await kit_reset(user_id, password)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    response.delete_cookie(TOKEN)

    return response
