from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.tracked import Tracked, TrackedData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time

__all__ = ("Named", "NamedData")


class NamedData(TrackedData):
    name: str


@define(kw_only=True)
class Named(Tracked):
    name: str

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            name=object.name,
        )

    @classmethod
    def from_data(cls, data: NamedData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> NamedData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
