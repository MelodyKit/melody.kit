from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app, config

__all__ = ("redirect_email",)

EMAIL = "{name}@{domain}"
email = EMAIL.format

EMAIL_TO = "mailto:"


def email_to(email: str) -> str:
    return EMAIL_TO + email


@app.get("/email/{name}")
async def redirect_email(name: str) -> RedirectResponse:
    return RedirectResponse(
        email_to(email(name=name, domain=config.domain)), status_code=status.HTTP_302_FOUND
    )
