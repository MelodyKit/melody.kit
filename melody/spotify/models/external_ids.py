from typing import Optional, Type, TypeVar

from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("ExternalIDs", "ExternalIDsData")


class ExternalIDsData(BaseData, total=False):
    isrc: str
    ean: str
    upc: str


E = TypeVar("E", bound="ExternalIDs")


@define()
class ExternalIDs(Base):
    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None

    @classmethod
    def from_data(cls: Type[E], data: ExternalIDsData) -> E:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExternalIDsData:
        return CONVERTER.unstructure(self)  # type: ignore


CONVERTER.register_unstructure_hook(
    ExternalIDs,
    make_dict_unstructure_fn(
        ExternalIDs,
        CONVERTER,
        isrc=override(omit_if_default=True),
        ean=override(omit_if_default=True),
        upc=override(omit_if_default=True),
    )
)
