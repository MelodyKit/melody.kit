from typing import Type, TypeVar, overload

from attrs import define
from edgedb import Object  # type: ignore

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER

__all__ = (
    "UserInfo",
    "UserInfoData",
    "user_info_from_object",
    "user_info_from_data",
    "user_info_into_data",
)


class UserInfoData(BaseData):
    verified: bool
    email: str
    password_hash: str


UI = TypeVar("UI", bound="UserInfo")


@define()
class UserInfo(Base):
    verified: bool
    email: str
    password_hash: str

    @classmethod
    def from_object(cls: Type[UI], object: Object) -> UI:  # type: ignore
        return cls(
            id=object.id,
            verified=object.verified,
            email=object.email,
            password_hash=object.password_hash,
        )

    @classmethod
    def from_data(cls: Type[UI], data: UserInfoData) -> UI:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserInfoData:
        return CONVERTER.unstructure(self)  # type: ignore

    def is_verified(self) -> bool:
        return self.verified


@overload
def user_info_from_object(object: Object) -> UserInfo:  # type: ignore
    ...


@overload
def user_info_from_object(object: Object, user_info_type: Type[UI]) -> UI:  # type: ignore
    ...


def user_info_from_object(
    object: Object, user_info_type: Type[UserInfo] = UserInfo  # type: ignore
) -> UserInfo:
    return UserInfo.from_object(object)


@overload
def user_info_from_data(data: UserInfoData) -> UserInfo:
    ...


@overload
def user_info_from_data(data: UserInfoData, user_info_type: Type[UI]) -> UI:
    ...


def user_info_from_data(data: UserInfoData, user_info_type: Type[UserInfo] = UserInfo) -> UserInfo:
    return user_info_type.from_data(data)


def user_info_into_data(user_info: UserInfo) -> UserInfoData:
    return user_info.into_data()
