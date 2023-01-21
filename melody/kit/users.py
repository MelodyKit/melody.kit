from uuid import UUID

from fastapi import Depends, status

from melody.kit.constants import ME
from melody.kit.core import database, v1
from melody.kit.dependencies import token_dependency
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import UserData

__all__ = ("get_self", "get_user")

CAN_NOT_FIND_USER = "can not find the user with id `{}`"


@v1.get(f"/users/{ME}")
async def get_self(user_id: UUID = Depends(token_dependency)) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()
