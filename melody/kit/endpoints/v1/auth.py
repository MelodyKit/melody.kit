from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import Body, Depends
from fastapi.responses import FileResponse
from pyotp import TOTP
from typing_aliases import NormalError

from melody.kit.code import generate_code
from melody.kit.core import database, hasher, v1
from melody.kit.dependencies import (
    BoundToken,
    access_token_dependency,
    bound_access_token_dependency,
    bound_refresh_token_dependency,
    bound_verification_token_dependency,
    email_deliverability_dependency,
    email_dependency,
)
from melody.kit.email import email_message, send_email_message, support
from melody.kit.errors import Conflict, NotFound, Unauthorized
from melody.kit.models.base import BaseData
from melody.kit.secrets import (
    delete_secret_for,
    fetch_secret_for,
    generate_secret_for,
    provisioning_url,
    secret_image_name,
)
from melody.kit.tags import AUTH, LINKS
from melody.kit.tokens import (
    delete_access_token,
    delete_access_tokens_for,
    delete_refresh_token,
    delete_refresh_tokens_for,
    delete_verification_token,
    generate_tokens_for,
    generate_verification_token_for,
)
from melody.shared.tokens import TokensData

__all__ = (
    # TOTP
    "get_totp",
    "get_totp_link",
    "generate_totp",
    "delete_totp",
    "verify_totp",
    # auth
    "login",
    "logout",
    "refresh",
    "revoke",
    "register",
    "verify",
    "reset",
    "forgot",
)

CAN_NOT_FIND_USER_BY_EMAIL = "can not find the user with the email `{}`"
can_not_find_user_by_email = CAN_NOT_FIND_USER_BY_EMAIL.format

PASSWORD_MISMATCH = "password mismatch"

UNVERIFIED = "user with ID `{}` is not verified"
unverified = UNVERIFIED.format

CAN_NOT_FIND_USER = "can not find the user with the ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format

CAN_NOT_FIND_SECRET = "can not find the secret for the user with the ID `{}`"
can_not_find_secret = CAN_NOT_FIND_SECRET.format

CODE_MISMATCH = "code mismatch"


@v1.get("/totp", tags=[AUTH], summary="Fetches TOTP secrets.")
async def get_totp(user_id: UUID = Depends(access_token_dependency)) -> str:
    user_info = await database.query_user_info(user_id=user_id)

    if user_info is None:
        raise NotFound(can_not_find_user(user_id))

    secret = user_info.secret

    if secret is None:
        raise NotFound(can_not_find_secret(user_id))

    return secret


@v1.get("/totp/link", tags=[AUTH, LINKS], summary="Fetches TOTP links.")
async def get_totp_link(user_id: UUID = Depends(access_token_dependency)) -> FileResponse:
    secret = await fetch_secret_for(user_id)

    if secret is None:
        secret = await get_totp(user_id=user_id)

    url = provisioning_url(user_id=user_id, secret=secret)

    image_name = secret_image_name(user_id)

    path = await generate_code(str(url), image_name)

    return FileResponse(path)


@v1.post("/totp", tags=[AUTH], summary="Generates TOTP secrets.")
async def generate_totp(user_id: UUID = Depends(access_token_dependency)) -> str:
    secret = await generate_secret_for(user_id)

    return secret


@v1.delete(
    "/totp",
    tags=[AUTH],
    summary="Deletes TOTP secrets",
)
async def delete_totp(user_id: UUID = Depends(access_token_dependency)) -> None:
    await database.update_user_secret(user_id=user_id, secret=None)


@v1.post(
    "/totp/verify",
    tags=[AUTH],
    summary="Verifies TOTP secrets.",
)
async def verify_totp(user_id: UUID = Depends(access_token_dependency), code: str = Body()) -> None:
    secret = await fetch_secret_for(user_id)

    if secret is None:
        raise NotFound(can_not_find_secret(user_id))

    totp = TOTP(secret)

    if not totp.verify(code):
        raise Unauthorized(CODE_MISMATCH)

    await delete_secret_for(user_id)

    await database.update_user_secret(user_id=user_id, secret=secret)


def verify_code(secret: Optional[str], code: Optional[str]) -> bool:
    if secret is None:
        return True

    if code is None:
        return False

    totp = TOTP(secret)

    return totp.verify(code)


@v1.post(
    "/login",
    tags=[AUTH],
    summary="Logs in the user with the given email and password.",
)
async def login(
    email: str = Depends(email_dependency),
    password: str = Body(),
    code: Optional[str] = Body(default=None),
) -> TokensData:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise NotFound(CAN_NOT_FIND_USER.format(email))

    user_id = user_info.id

    if not user_info.is_verified():
        raise Unauthorized(UNVERIFIED.format(user_id))

    password_hash = user_info.password_hash

    try:
        hasher.verify(password_hash, password)

    except VerifyMismatchError:
        raise Unauthorized(PASSWORD_MISMATCH) from None

    secret = user_info.secret

    if not verify_code(secret, code):
        raise Unauthorized(CODE_MISMATCH)

    tokens = await generate_tokens_for(user_id)

    if hasher.check_needs_rehash(password_hash):
        password_hash = hasher.hash(password)

        await database.update_user_password_hash(user_id=user_id, password_hash=password_hash)

    return tokens.into_data()


@v1.post(
    "/logout",
    tags=[AUTH],
    summary="Logs out the user, revoking the current token.",
)
async def logout(
    bound_token: BoundToken = Depends(bound_access_token_dependency),
) -> None:
    await delete_access_token(bound_token.token)


@v1.post(
    "/refresh",
    tags=[AUTH],
    summary="Refreshes the access token.",
)
async def refresh(
    bound_token: BoundToken = Depends(bound_refresh_token_dependency),
) -> TokensData:
    await delete_refresh_token(bound_token.token)

    tokens = await generate_tokens_for(bound_token.user_id)

    return tokens.into_data()


@v1.post(
    "/revoke",
    tags=[AUTH],
    summary="Revokes all tokens of the user.",
)
async def revoke(user_id: UUID = Depends(access_token_dependency)) -> None:
    await delete_access_tokens_for(user_id)
    await delete_refresh_tokens_for(user_id)


EMAIL_TAKEN = "the email `{}` is taken"

VERIFICATION = "MelodyKit verification token"
VERIFICATION_CONTENT = """
Here is your verification token:

{verification_token}
""".strip()
verification_content = VERIFICATION_CONTENT.format


@v1.post(
    "/register",
    tags=[AUTH],
    summary="Registers the user with the given name, email and password.",
)
async def register(
    name: str = Body(),
    email: str = Depends(email_deliverability_dependency),
    password: str = Body(),
) -> BaseData:
    password_hash = hasher.hash(password)

    try:
        base = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise Conflict(EMAIL_TAKEN.format(email)) from None

    else:
        user_id = base.id

        verification_token = await generate_verification_token_for(user_id)

        try:
            await send_email_message(
                email_message(
                    author=support(),
                    target=email,
                    subject=VERIFICATION,
                    content=verification_content(verification_token=verification_token),
                )
            )

        except NormalError:
            await database.delete_user(user_id=user_id)
            await delete_verification_token(verification_token)

            raise

        return base.into_data()


VERIFICATION_NOT_FOUND = "verification for the user not found"


@v1.post(
    "/verify",
    tags=[AUTH],
    summary="Verifies the user with the given ID.",
)
async def verify(bound_token: BoundToken = Depends(bound_verification_token_dependency)) -> None:
    await delete_verification_token(bound_token.token)

    await database.update_user_verified(user_id=bound_token.user_id, verified=True)


@v1.post(
    "/reset",
    tags=[AUTH],
    summary="Resets the password of the user, revoking all tokens.",
)
async def reset(user_id: UUID = Depends(access_token_dependency), password: str = Body()) -> None:
    await revoke(user_id)

    password_hash = hasher.hash(password)

    await database.update_user_password_hash(user_id=user_id, password_hash=password_hash)


CAN_NOT_FIND_USER_BY_EMAIL = "can not find the user with the email `{}`"


TEMPORARY_TOKEN = "MelodyKit temporary token"
TEMPORARY_TOKEN_CONTENT = """
Here is your temporary token:

{temporary_token}
""".strip()
temporary_token_content = TEMPORARY_TOKEN_CONTENT.format


@v1.post(
    "/forgot",
    tags=[AUTH],
    summary="Allows the user to reset their password via the email.",
)
async def forgot(email: str = Depends(email_dependency)) -> None:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise NotFound(CAN_NOT_FIND_USER_BY_EMAIL.format(email))

    tokens = await generate_tokens_for(user_info.id)

    temporary_token = tokens.access_token

    await send_email_message(
        email_message(
            author=support(),
            target=email,
            subject=TEMPORARY_TOKEN,
            content=temporary_token_content(temporary_token=temporary_token),
        )
    )
