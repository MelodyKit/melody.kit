from typing import Type, TypeVar

from attrs import define
from edgedb import Object  # type: ignore

from melody.kit.models.abstract import Abstract, AbstractData

__all__ = ("UserInfo", "UserInfoData", "user_info_from_object", "user_info_into_data")


class UserInfoData(AbstractData):
    verified: bool
    email: str
    password_hash: str


UI = TypeVar("UI", bound="UserInfo")


@define()
class UserInfo(Abstract):
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

    def into_data(self) -> UserInfoData:
        return UserInfoData(
            id=str(self.id),
            verified=self.verified,
            email=self.email,
            password_hash=self.password_hash,
        )

    def is_verified(self) -> bool:
        return self.verified


def user_info_from_object(object: Object) -> UserInfo:
    return UserInfo.from_object(object)


def user_info_into_data(user_info: UserInfo) -> UserInfoData:
    return user_info.into_data()
