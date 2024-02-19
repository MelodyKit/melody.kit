from fastapi.responses import FileResponse

from melody.kit.code import generate_code
from melody.kit.core import database, v1
from melody.kit.enums import Tag
from melody.kit.errors.auth import AuthCodeConflict, AuthCodeNotFound, AuthUserNotFound
from melody.kit.tokens.dependencies import UserTokenDependency
from melody.kit.totp.core import validate_totp
from melody.kit.totp.dependencies import CodeDependency, OptionalCodeDependency
from melody.kit.totp.operations import delete_secret_for, fetch_secret_for, generate_secret_for
from melody.kit.totp.provisioning import provisioning_image_name, provisioning_url
from melody.shared.converter import unstructure_url

__all__ = (
    "generate_totp",
    "remove_totp",
    "link_totp",
    "verify_totp",
)

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format

CAN_NOT_FIND_SECRET = "can not find the secret for the user with ID `{}`"
can_not_find_secret = CAN_NOT_FIND_SECRET.format

TOTP_ALREADY_ENABLED = "TOTP is already enabled"


@v1.post("/totp", tags=[Tag.TOTP], summary="Generates TOTP secrets.")
async def generate_totp(context: UserTokenDependency) -> str:
    self_id = context.user_id

    self_info = await database.query_user_info(user_id=self_id)

    if self_info is None:
        raise AuthUserNotFound(self_id)

    if self_info.is_totp_enabled():
        raise AuthCodeConflict()

    secret = await fetch_secret_for(self_id)

    if secret is None:
        secret = await generate_secret_for(self_id)

    return secret


@v1.delete(
    "/totp",
    tags=[Tag.TOTP],
    summary="Removes TOTP secrets.",
)
async def remove_totp(context: UserTokenDependency, code: OptionalCodeDependency = None) -> None:
    self_id = context.user_id

    self_info = await database.query_user_info(user_id=self_id)

    if self_info is None:
        raise AuthUserNotFound(self_id)

    secret = self_info.secret

    validate_totp(secret, code)

    await database.update_user_secret(user_id=context.user_id, secret=None)


@v1.get("/totp/link", tags=[Tag.TOTP], summary="Fetches TOTP links.")
async def link_totp(context: UserTokenDependency) -> FileResponse:
    self_id = context.user_id

    secret = await fetch_secret_for(self_id)

    if secret is None:
        raise AuthCodeNotFound()

    url = provisioning_url(user_id=self_id, secret=secret)

    image_name = provisioning_image_name(secret)

    path = await generate_code(unstructure_url(url), image_name)

    return FileResponse(path)


@v1.post(
    "/totp/verify",
    tags=[Tag.TOTP],
    summary="Verifies TOTP secrets.",
)
async def verify_totp(context: UserTokenDependency, code: CodeDependency) -> None:
    self_id = context.user_id

    secret = await fetch_secret_for(self_id)

    if secret is None:
        raise AuthCodeNotFound()

    validate_totp(secret, code)

    await delete_secret_for(self_id)

    await database.update_user_secret(user_id=self_id, secret=secret)
