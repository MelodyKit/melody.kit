from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError, NoDataError
from fastapi import status

from melody.kit.core import database, hasher, v1
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import AbstractData
from melody.kit.tokens import TokenData, decode_token, encode_token

__all__ = ("login", "logout", "register")

CAN_NOT_FIND_USER = "can not find the user with the email `{}`"
PASSWORD_MISMATCH = "password mismatch"


@v1.get("/login")
async def login(email: str, password: str) -> TokenData:
    try:
        user_info = await database.query_user_info_by(email=email)

    except NoDataError:
        raise Error(
            status.HTTP_404_NOT_FOUND, ErrorCode.NOT_FOUND, CAN_NOT_FIND_USER.format(email)
        ) from None

    else:
        try:
            hasher.verify(user_info.password_hash, password)

        except VerifyMismatchError:
            raise Error(
                status.HTTP_401_UNAUTHORIZED, ErrorCode.UNAUTHORIZED, PASSWORD_MISMATCH
            ) from None

        else:
            token = encode_token(user_info.id)

            return TokenData(token=token)


@v1.get("/logout")
async def logout(token: str) -> None:
    ...


EMAIL_TAKEN = "the email `{}` is taken"


@v1.get("/register")
async def register(name: str, email: str, password: str) -> AbstractData:
    password_hash = hasher.hash(password)

    try:
        abstract = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise Error(
            status.HTTP_409_CONFLICT, ErrorCode.CONFLICT, EMAIL_TAKEN.format(email)
        ) from None

    else:
        return abstract.into_data()
