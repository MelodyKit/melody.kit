from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import Body, Depends
from typing_aliases import NormalError

from melody.kit.core import database, hasher, v1
from melody.kit.dependencies import (
    bound_verification_token_dependency,
    email_deliverability_dependency,
    email_dependency,
)
from melody.kit.email import email_message, send_email_message, support
from melody.kit.endpoints.v1.totp import validate_totp
from melody.kit.errors import Conflict, NotFound, Unauthorized
from melody.kit.models.base import BaseData
from melody.kit.oauth2 import (
    ClientCredentials,
    bound_token_dependency,
    client_credentials_dependency,
    token_dependency,
)
from melody.kit.tags import AUTH
from melody.kit.tokens import (
    BoundToken,
    delete_access_token,
    delete_access_tokens_for,
    delete_refresh_tokens_for,
    delete_verification_token,
    generate_tokens_for,
    generate_verification_token_for,
)
from melody.shared.enums import GrantType
from melody.shared.tokens import TokensData

__all__ = (
    "login",
    "logout",
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

    validate_totp(secret, code)

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
    bound_token: BoundToken = Depends(bound_token_dependency),
) -> None:
    await delete_access_token(bound_token.token)


@v1.post("/tokens", tags=[AUTH], summary="Generates tokens.")
async def generate_tokens(
    grant_type: GrantType,
    code: Optional[str] = None,
    refresh_token: Optional[str] = None,
    client_credentials: ClientCredentials = Depends(client_credentials_dependency),
) -> None:
    if grant_type.is_authorization_code():
        ...

    if grant_type.is_client_credentials():
        ...

    if grant_type.is_refresh_token():
        ...


@v1.post(
    "/revoke",
    tags=[AUTH],
    summary="Revokes all tokens of the user.",
)
async def revoke(self_id: UUID = Depends(token_dependency)) -> None:
    await delete_access_tokens_for(self_id)
    await delete_refresh_tokens_for(self_id)


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
        self = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise Conflict(EMAIL_TAKEN.format(email)) from None

    else:
        self_id = self.id

        verification_token = await generate_verification_token_for(self_id)

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
            await database.delete_user(user_id=self_id)
            await delete_verification_token(verification_token)

            raise

        return self.into_data()


VERIFICATION_NOT_FOUND = "verification for the user not found"


@v1.post(
    "/verify",
    tags=[AUTH],
    summary="Verifies the user with the given ID.",
)
async def verify(bound_token: BoundToken = Depends(bound_verification_token_dependency)) -> None:
    await delete_verification_token(bound_token.token)

    await database.update_user_verified(user_id=bound_token.self_id, verified=True)


@v1.post(
    "/reset",
    tags=[AUTH],
    summary="Resets the password of the user, revoking all tokens.",
)
async def reset(self_id: UUID = Depends(token_dependency), password: str = Body()) -> None:
    await revoke(self_id)

    password_hash = hasher.hash(password)

    await database.update_user_password_hash(user_id=self_id, password_hash=password_hash)


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
