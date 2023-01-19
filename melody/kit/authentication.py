from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError, NoDataError
from fastapi import Depends, status

from melody.kit.core import database, hasher, v1
from melody.kit.dependencies import token_dependency
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import AbstractData
from melody.kit.tokens import TokenData, encode_token

__all__ = ("login", "logout", "register")

CAN_NOT_FIND_USER = "can not find the user with the email `{}`"
PASSWORD_MISMATCH = "password mismatch"


@v1.get("/login")
async def login(email: str, password: str) -> TokenData:
    try:
        user_info = await database.query_user_info_by(email=email)

    except NoDataError:
        raise Error(
            CAN_NOT_FIND_USER.format(email), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        ) from None

    else:
        password_hash = user_info.password_hash

        try:
            hasher.verify(password_hash, password)

        except VerifyMismatchError:
            raise Error(
                PASSWORD_MISMATCH, ErrorCode.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED
            ) from None

        else:
            user_id = user_info.id

            token = encode_token(user_id)

            if hasher.check_needs_rehash(password_hash):
                password_hash = hasher.hash(password)

                await database.update_password_hash(user_id=user_id, password_hash=password_hash)

            return TokenData(token=token)


@v1.get("/logout")
async def logout(user_id: UUID = Depends(token_dependency)) -> None:
    ...


EMAIL_TAKEN = "the email `{}` is taken"


@v1.get("/register")
async def register(name: str, email: str, password: str) -> AbstractData:
    password_hash = hasher.hash(password)

    try:
        abstract = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise Error(
            EMAIL_TAKEN.format(email), ErrorCode.CONFLICT, status.HTTP_409_CONFLICT
        ) from None

    else:
        return abstract.into_data()
