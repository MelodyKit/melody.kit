from typing import Optional, Type
from typing import TypedDict as Data
from typing import TypeVar, overload

from attrs import define
from yarl import URL

from melody.kit.constants import DEFAULT_COUNT
from melody.shared.converter import CONVERTER

__all__ = (
    "PaginationData",
    "Pagination",
    "pagination_from_data",
    "pagination_into_data",
    "paginate",
)


class PaginationData(Data):
    previous: Optional[str]
    next: Optional[str]
    count: int


P = TypeVar("P", bound="Pagination")


@define()
class Pagination:
    previous: Optional[URL] = None
    next: Optional[URL] = None
    count: int = DEFAULT_COUNT

    @classmethod
    def paginate(cls: Type[P], url: URL, offset: int, limit: int, count: int) -> P:
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
    def from_data(cls: Type[P], data: PaginationData) -> P:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PaginationData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def pagination_from_data(data: PaginationData) -> Pagination:
    ...


@overload
def pagination_from_data(data: PaginationData, pagination_type: Type[P]) -> P:
    ...


def pagination_from_data(
    data: PaginationData, pagination_type: Type[Pagination] = Pagination
) -> Pagination:
    return pagination_type.from_data(data)


def pagination_into_data(pagination: Pagination) -> PaginationData:
    return pagination.into_data()


@overload
def paginate(url: URL, offset: int, limit: int, count: int) -> Pagination:
    ...


@overload
def paginate(url: URL, offset: int, limit: int, count: int, pagination_type: Type[P]) -> P:
    ...


def paginate(
    url: URL, offset: int, limit: int, count: int, pagination_type: Type[Pagination] = Pagination
) -> Pagination:
    return pagination_type.paginate(url=url, offset=offset, limit=limit, count=count)


def unstructure_url(url: URL) -> str:
    return url.human_repr()


def structure_url_ignore_type(string: str, url_type: Type[URL]) -> URL:
    return URL(string)


CONVERTER.register_structure_hook(URL, structure_url_ignore_type)
CONVERTER.register_unstructure_hook(URL, unstructure_url)
