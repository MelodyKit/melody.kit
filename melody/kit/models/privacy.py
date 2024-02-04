from uuid import UUID

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.enums import PrivacyType
from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER
from melody.shared.markers import unreachable

__all__ = ("UserPrivacy", "UserPrivacyData", "PlaylistPrivacy", "PlaylistPrivacyData")


class UserPrivacyData(BaseData):
    privacy_type: str


@define()
class UserPrivacy(Base):
    privacy_type: PrivacyType

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(id=object.id, privacy_type=PrivacyType(object.privacy_type.value))

    @classmethod
    def from_data(cls, data: UserPrivacyData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserPrivacyData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    def is_accessible(self) -> bool:
        return self.privacy_type.is_public()

    def is_accessible_by(self, user_id: UUID, friends: bool) -> bool:
        if self.id == user_id:
            return True

        privacy_type = self.privacy_type

        if privacy_type.is_public():
            return True

        if privacy_type.is_friends():
            return friends

        if privacy_type.is_private():
            return False

        unreachable()  # all `PrivacyType` variants have been handled


class PlaylistPrivacyData(BaseData):
    privacy_type: str
    owner: UserPrivacyData


@define()
class PlaylistPrivacy(Base):
    privacy_type: PrivacyType
    owner: UserPrivacy

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            privacy_type=PrivacyType(object.privacy_type.value),
            owner=UserPrivacy.from_object(object.owner),
        )

    @classmethod
    def from_data(cls, data: PlaylistPrivacyData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistPrivacyData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    def is_accessible(self) -> bool:
        return self.owner.is_accessible() and self.privacy_type.is_public()

    def is_accessible_by(self, user_id: UUID, friends: bool) -> bool:
        if not self.owner.is_accessible_by(user_id, friends):
            return False

        privacy_type = self.privacy_type

        if privacy_type.is_public():
            return True

        if privacy_type.is_friends():
            return friends

        if privacy_type.is_private():
            return False

        unreachable()  # all `PrivacyType` variants have been handled
