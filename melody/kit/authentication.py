from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import Depends, status

from melody.kit.core import database, hasher, tokens, v1
from melody.kit.dependencies import token_dependency
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import AbstractData
from melody.kit.tokens import TokenData, encode_token
from melody.kit.utils import utc_now

__all__ = ("login", "logout", "register")

CAN_NOT_FIND_USER = "can not find the user with the email `{}`"
PASSWORD_MISMATCH = "password mismatch"

UNVERIFIED = "user with id `{}` is not verified"


@v1.get("/login")
async def login(email: str, password: str) -> TokenData:
    user_info = await database.query_user_info_by_email(email)

    if user_info is None:
        raise Error(
            CAN_NOT_FIND_USER.format(email), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    user_id = user_info.id

    if not user_info.is_verified():
        raise Error(
            UNVERIFIED.format(user_id), ErrorCode.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED
        )

    password_hash = user_info.password_hash

    try:
        hasher.verify(password_hash, password)

    except VerifyMismatchError:
        raise Error(
            PASSWORD_MISMATCH, ErrorCode.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED
        ) from None

    else:
        token = encode_token(user_id)

        if hasher.check_needs_rehash(password_hash):
            password_hash = hasher.hash(password)

            await database.update_user_password_hash(user_id, password_hash)

        return TokenData(token=token)


@v1.get("/logout")
async def logout(user_id: UUID = Depends(token_dependency)) -> None:
    tokens[user_id] = utc_now()


EMAIL_TAKEN = "the email `{}` is taken"


@v1.get("/register")
async def register(name: str, email: str, password: str) -> AbstractData:
    password_hash = hasher.hash(password)

    try:
        abstract = await database.insert_user(name, email, password_hash)

    except ConstraintViolationError:
        raise Error(
            EMAIL_TAKEN.format(email), ErrorCode.CONFLICT, status.HTTP_409_CONFLICT
        ) from None

    else:
        return abstract.into_data()
