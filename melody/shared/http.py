from __future__ import annotations

from atexit import register as register_at_exit
from typing import Any, ClassVar, List, Optional, overload

from async_extensions.run import run
from attrs import define, field, frozen
from httpx import AsyncClient, HTTPError
from typing_extensions import Literal

from melody.shared.constants import DEFAULT_RETRIES, NAME, PYTHON
from melody.shared.enums import ResponseType
from melody.shared.typing import Headers, Parameters, Payload, Response
from melody.versions import python_version_info, version_info

__all__ = ("HTTPClient", "Route")

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


USER_AGENT_LITERAL = "User-Agent"
USER_AGENT = f"{NAME}/{version_info} ({PYTHON}/{python_version_info})"

HEADERS = {USER_AGENT_LITERAL: USER_AGENT}


@define()
class HTTPClient:
    USER_AGENT: ClassVar[str] = USER_AGENT

    client: AsyncClient = field(factory=AsyncClient)

    retries: int = field(default=DEFAULT_RETRIES)

    def __attrs_post_init__(self) -> None:
        add_client(self)

        self.client.headers.update(HEADERS)

    async def close(self) -> None:
        await self.client.aclose()

    @overload
    async def request(
        self,
        method: str,
        path: str,
        response_type: Literal[ResponseType.JSON] = ...,
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> Payload:
        ...

    @overload
    async def request(
        self,
        method: str,
        path: str,
        response_type: Literal[ResponseType.TEXT],
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> str:
        ...

    @overload
    async def request(
        self,
        method: str,
        path: str,
        response_type: Literal[ResponseType.BYTES],
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> bytes:
        ...

    @overload
    async def request(
        self,
        method: str,
        path: str,
        response_type: ResponseType,
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> Response:
        ...

    async def request(
        self,
        method: str,
        path: str,
        response_type: ResponseType = ResponseType.JSON,
        payload: Optional[Payload] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        attempts = self.retries + 1

        if parameters is None:
            parameters = {}

        else:
            parameters = {name: str(value) for name, value in parameters.items()}

        if headers is None:
            headers = {}

        else:
            headers = {name: str(value) for name, value in headers.items()}

        error: Optional[HTTPError] = None

        while attempts:
            try:
                response = await self.client.request(
                    method, path, json=payload, params=parameters, headers=headers
                )

                response.raise_for_status()

            except HTTPError as origin:
                error = origin

            else:
                if response_type.is_json():
                    return response.json()  # type: ignore

                if response_type.is_text():
                    return response.text

                return response.read()

            attempts -= 1

        if error:
            raise error

        return None  # pragma: never

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: Literal[ResponseType.JSON] = ...,
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> Payload:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: Literal[ResponseType.TEXT],
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> str:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: Literal[ResponseType.BYTES],
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> bytes:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: ResponseType,
        payload: Optional[Payload] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
    ) -> Response:
        ...

    async def request_route(
        self,
        route: Route,
        response_type: ResponseType = ResponseType.JSON,
        payload: Optional[Payload] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        return await self.request(
            route.method,
            route.path,
            response_type=response_type,
            payload=payload,
            parameters=parameters,
            headers=headers,
        )


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
