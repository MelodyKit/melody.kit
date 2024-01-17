from typing import Optional

from attrs import define
from typing_extensions import Self
from yarl import URL

from melody.kit.constants import DEFAULT_COUNT
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("Pagination", "PaginationData")


class PaginationData(Data):
    previous: Optional[str]
    next: Optional[str]
    count: int


@define()
class Pagination:
    previous: Optional[URL] = None
    next: Optional[URL] = None
    count: int = DEFAULT_COUNT

    @classmethod
    def paginate(cls, url: URL, offset: int, limit: int, count: int) -> Self:
        after = offset + limit

        if after < count:
            next = url.update_query(offset=after, limit=limit)

        else:
            next = None

        before = offset - limit

        if before < 0:
            before = 0

        if offset:
            previous = url.update_query(offset=before, limit=limit)

        else:
            previous = None

        return cls(previous=previous, next=next, count=count)

    @classmethod
    def from_data(cls, data: PaginationData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PaginationData:
        return CONVERTER.unstructure(self)  # type: ignore
