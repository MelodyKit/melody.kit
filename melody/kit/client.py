from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

__all__ = ("Client",)


@define()
class Client:
    database: AsyncIOClient = field(factory=create_async_client)
