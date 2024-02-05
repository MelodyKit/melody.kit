from typing import Optional
from uuid import UUID

from fastapi import Body, Depends
from fastapi.responses import FileResponse
from pyotp import TOTP

from melody.kit.code import generate_code
from melody.kit.core import database, v1
from melody.kit.enums import Tag
from melody.kit.errors import NotFound, Unauthorized
from melody.kit.oauth2 import token_dependency
from melody.kit.totp import (
    delete_secret_for,
    fetch_secret_for,
    generate_secret_for,
    provisioning_url,
    secret_image_name,
)

__all__ = (
    "validate_totp",
    "generate_totp",
    "delete_totp",
    "link_totp",
    "verify_totp",
)

CAN_NOT_FIND_SECRET = "can not find the secret for the user with ID `{}`"
can_not_find_secret = CAN_NOT_FIND_SECRET.format

CODE_MISMATCH = "code mismatch"
EXPECTED_CODE = "expected code"


def validate_totp(secret: Optional[str], code: Optional[str]) -> None:
    if secret is None:
        return

    if code is None:
        raise Unauthorized(EXPECTED_CODE)

    totp = TOTP(secret)

    if not totp.verify(code):
        raise Unauthorized(CODE_MISMATCH)


@v1.post("/totp", tags=[Tag.TOTP], summary="Generates TOTP secrets.")
async def generate_totp(self_id: UUID = Depends(token_dependency)) -> str:
    secret = await fetch_secret_for(self_id)

    if secret is None:
        secret = await generate_secret_for(self_id)

    return secret


@v1.delete(
    "/totp",
    tags=[Tag.TOTP],
    summary="Deletes TOTP secrets/",
)
async def delete_totp(self_id: UUID = Depends(token_dependency)) -> None:
    await database.update_user_secret(user_id=self_id, secret=None)


@v1.get("/totp/link", tags=[Tag.TOTP], summary="Fetches TOTP links.")
async def link_totp(self_id: UUID = Depends(token_dependency)) -> FileResponse:
    secret = await fetch_secret_for(self_id)

    if secret is None:
        raise NotFound(can_not_find_secret(self_id))

    url = provisioning_url(user_id=self_id, secret=secret)

    image_name = secret_image_name(secret)

    path = await generate_code(str(url), image_name)

    return FileResponse(path)


@v1.post(
    "/totp/verify",
    tags=[Tag.TOTP],
    summary="Verifies TOTP secrets.",
)
async def verify_totp(self_id: UUID = Depends(token_dependency), code: str = Body()) -> None:
    secret = await fetch_secret_for(self_id)

    if secret is None:
        raise NotFound(can_not_find_secret(self_id))

    validate_totp(secret, code)

    await delete_secret_for(self_id)

    await database.update_user_secret(user_id=self_id, secret=secret)
