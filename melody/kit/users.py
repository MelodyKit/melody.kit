from uuid import UUID

from edgedb import NoDataError
from fastapi import status

from melody.kit.core import database, v1
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import UserData

__all__ = ("get_user",)

CAN_NOT_FIND_USER = "can not find the user with id `{}`"


@v1.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserData:
    try:
        user = await database.query_user(user_id)

    except NoDataError:
        raise Error(
            status.HTTP_404_NOT_FOUND, ErrorCode.NOT_FOUND, CAN_NOT_FIND_USER.format(user_id)
        ) from None

    else:
        return user.into_data()
