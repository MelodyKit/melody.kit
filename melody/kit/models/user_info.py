from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER

__all__ = ("UserInfo", "UserInfoData")


class UserInfoData(BaseData):
    verified: bool
    email: str
    password_hash: str


@define()
class UserInfo(Base):
    verified: bool
    email: str
    password_hash: str

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            verified=object.verified,
            email=object.email,
            password_hash=object.password_hash,
        )

    @classmethod
    def from_data(cls, data: UserInfoData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserInfoData:
        return CONVERTER.unstructure(self)  # type: ignore

    def is_verified(self) -> bool:
        return self.verified
