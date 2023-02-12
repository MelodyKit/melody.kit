from email.message import EmailMessage
from uuid import UUID

from aiosmtplib import SMTP
from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import Body, Depends

from melody.kit.core import config, database, hasher, v1, verification_tokens
from melody.kit.dependencies import (
    BoundToken,
    bound_token_dependency,
    email_deliverability_dependency,
    email_dependency,
    token_dependency,
)
from melody.kit.errors import Conflict, NotFound, Unauthorized
from melody.kit.models.base import BaseData, base_into_data
from melody.kit.tags import AUTHENTICATION
from melody.kit.tokens import (
    TokenData,
    delete_token,
    delete_tokens_for,
    generate_token,
    token_factory,
    token_into_data,
)

__all__ = ("login", "logout", "revoke", "register", "verify", "reset")

CAN_NOT_FIND_USER = "can not find the user with the email `{}`"
PASSWORD_MISMATCH = "password mismatch"

UNVERIFIED = "user with ID `{}` is not verified"


@v1.post(
    "/login",
    tags=[AUTHENTICATION],
    summary="Logs in the user with the given email and password.",
)
async def login(email: str = Depends(email_dependency), password: str = Body()) -> TokenData:
    user_info = await database.query_user_info_by_email(email)

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

    else:
        token = await generate_token(user_id)

        if hasher.check_needs_rehash(password_hash):
            password_hash = hasher.hash(password)

            await database.update_user_password_hash(user_id, password_hash)

        return token_into_data(token)


@v1.post(
    "/logout",
    tags=[AUTHENTICATION],
    summary="Logs out the user, revoking the current token.",
)
async def logout(bound_token: BoundToken = Depends(bound_token_dependency)) -> None:
    await delete_token(bound_token.token)


@v1.post(
    "/revoke",
    tags=[AUTHENTICATION],
    summary="Revokes all tokens of the user.",
)
async def revoke(user_id: UUID = Depends(token_dependency)) -> None:
    await delete_tokens_for(user_id)


EMAIL_TAKEN = "the email `{}` is taken"

FROM = "From"
TO = "To"
SUBJECT = "Subject"

FROM_FORMAT = "{name} <{email}>"

VERIFICATION = "Please verify your account"
CONTENT = """
Please verify your account by clicking the link below:

https://{domain}/verify/{user_id}/{verification_token}
""".strip()


@v1.post(
    "/register",
    tags=[AUTHENTICATION],
    summary="Registers the user with the given name, email and password.",
)
async def register(
    name: str = Body(),
    email: str = Depends(email_deliverability_dependency),
    password: str = Body(),
) -> BaseData:
    password_hash = hasher.hash(password)

    try:
        base = await database.insert_user(name, email, password_hash)

    except ConstraintViolationError:
        raise Conflict(EMAIL_TAKEN.format(email)) from None

    else:
        user_id = base.id
        verification_token = token_factory()

        message = EmailMessage()

        message[FROM] = FROM_FORMAT.format(name=config.name, email=config.email.support)

        message[TO] = email

        message[SUBJECT] = VERIFICATION

        message.set_content(
            CONTENT.format(
                domain=config.domain, user_id=user_id, verification_token=verification_token
            )
        )

        client = SMTP(
            config.email.host,
            config.email.port,
            config.email.name,
            config.email.password,
            start_tls=True,
        )

        try:
            async with client:
                await client.send_message(message)

        except Exception:
            await database.delete_user(user_id)

            raise

        verification_tokens[user_id] = verification_token

        return base_into_data(base)


VERIFICATION_TOKEN_MISMATCH = "verification token mismatch"
VERIFICATION_NOT_FOUND = "verification for the user with ID `{}` not found"


@v1.post(
    "/verify/{user_id}/{verification_token}",
    tags=[AUTHENTICATION],
    summary="Verifies the user with the given ID.",
)
async def verify(user_id: UUID, verification_token: str) -> None:
    if user_id in verification_tokens:
        if verification_tokens[user_id] == verification_token:
            del verification_tokens[user_id]

            await database.update_user_verified(user_id, True)

        else:
            raise Unauthorized(VERIFICATION_TOKEN_MISMATCH)

    else:
        raise NotFound(VERIFICATION_NOT_FOUND.format(user_id))


@v1.post(
    "/reset",
    tags=[AUTHENTICATION],
    summary="Resets the password of the user, revoking all tokens.",
)
async def reset(user_id: UUID = Depends(token_dependency), password: str = Body()) -> None:
    await revoke(user_id)

    password_hash = hasher.hash(password)

    await database.update_user_password_hash(user_id, password_hash)
