from typing import Optional

from attrs import define
from cattrs.gen import override
from typing_extensions import Self

from melody.shared.converter import CONVERTER, register_unstructure_hook
from melody.spotify.models.base import Base, BaseData

__all__ = ("ExternalIDs", "ExternalIDsData")


class ExternalIDsData(BaseData, total=False):
    isrc: str
    ean: str
    upc: str


register_unstructure_hook_omit_if_default = register_unstructure_hook(
    isrc=override(omit_if_default=True),
    ean=override(omit_if_default=True),
    upc=override(omit_if_default=True),
)


@register_unstructure_hook_omit_if_default
@define()
class ExternalIDs(Base):
    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None

    @classmethod
    def from_data(cls, data: ExternalIDsData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExternalIDsData:
        return CONVERTER.unstructure(self)  # type: ignore
