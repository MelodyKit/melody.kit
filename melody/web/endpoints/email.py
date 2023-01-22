from fastapi import status
from fastapi.responses import RedirectResponse

from melody.kit.core import app

__all__ = ("redirect_email",)

EMAIL = "{name}@{domain}"

EMAIL_TO = "mailto:"
DOMAIN = "melodykit.app"


@app.get("/email/{name}")
async def redirect_email(name: str) -> RedirectResponse:
    return RedirectResponse(EMAIL_TO + EMAIL.format(name=name, domain=DOMAIN), status_code=status.HTTP_302_FOUND)
