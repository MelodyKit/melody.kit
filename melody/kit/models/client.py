from typing import Optional

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.named import Named, NamedData
from melody.shared.converter import CONVERTER
from melody.shared.time import convert_standard_date_time

__all__ = ("Client", "ClientData")


class ClientData(NamedData):
    owner: NamedData
    description: Optional[str]


@define(kw_only=True)
class Client(Named):
    owner: Named
    description: Optional[str] = None

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            name=object.name,
            owner=Named.from_object(object.owner),
            description=object.description,
        )

    @classmethod
    def from_data(cls, data: ClientData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ClientData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
