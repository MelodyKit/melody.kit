from __future__ import annotations

from atexit import register as register_at_exit
from typing import Any, List

from async_extensions.run import run
from attrs import define, field, frozen
from httpx import AsyncClient, HTTPError

from melody.shared.constants import DEFAULT_RETRIES

__all__ = ("Route", "HTTPClient")

KEY = "{route.method} {route.path}"
key = KEY.format


@frozen()
class Route:
    method: str
    path: str

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.__attrs_init__(method, path.format_map(parameters))  # type: ignore

    @property
    def key(self) -> str:
        return key(route=self)


@define()
class HTTPClient:
    client: AsyncClient = field(factory=AsyncClient)

    retries: int = field(default=DEFAULT_RETRIES)

    async def close(self) -> None:
        await self.client.aclose()

    async def request(self, method: str, path: str) -> Any:
        try:
            response = await self.client.request(method, path)

        except HTTPError:
            ...

        else:
            return response.json()

    async def request_route(self, route: Route) -> Any:
        return await self.request(route.method, route.path)


CLIENTS: List[HTTPClient] = []


def add_client(client: HTTPClient) -> None:
    CLIENTS.append(client)


def remove_client(client: HTTPClient) -> None:
    CLIENTS.remove(client)


async def close_all_clients() -> None:
    for client in CLIENTS:
        await client.close()


def close_all_clients_sync() -> None:
    run(close_all_clients())


register_at_exit(close_all_clients_sync)
