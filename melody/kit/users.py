from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import FileResponse

from melody.kit.constants import ME
from melody.kit.core import database, v1
from melody.kit.dependencies import token_dependency
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import UserData
from melody.kit.uri import URI

__all__ = ("get_self", "get_self_link", "get_user", "get_user_link")

CAN_NOT_FIND_USER = "can not find the user with id `{}`"


@v1.get(f"/users/{ME}")
async def get_self(user_id: UUID = Depends(token_dependency)) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get(f"/users/{ME}/link")
async def get_self_link(user_id: UUID = Depends(token_dependency)) -> FileResponse:
    uri = URI(type=URIType.USER, id=user_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get("/users/{user_id}/link")
async def get_user_link(user_id: UUID) -> FileResponse:
    uri = URI(type=URIType.USER, id=user_id)

    path = await uri.create_link()

    return FileResponse(path)
