from uuid import UUID

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER

__all__ = ("ClientInfo", "ClientInfoData")


class ClientInfoData(BaseData):
    secret_hash: str


@define(kw_only=True)
class ClientInfo(Base):
    secret_hash: str
    owner_id: UUID

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(id=object.id, secret_hash=object.secret_hash, owner_id=object.owner.id)

    @classmethod
    def from_data(cls, data: ClientInfoData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ClientInfoData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
