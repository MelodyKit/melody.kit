from __future__ import annotations

from asyncio import run, sleep
from atexit import register as register_at_exit
from typing import Any, ClassVar, List, Literal, Optional, Union, overload

from aiohttp import BasicAuth, ClientError, ClientSession, ClientTimeout
from attrs import define, evolve, field, frozen
from typing_aliases import Headers, Parameters, Payload
from typing_extensions import Self
from yarl import URL

from melody.shared.constants import DEFAULT_RETRIES, DEFAULT_TIMEOUT, NAME, PYTHON, SLASH, ZERO
from melody.shared.enums import ResponseType
from melody.shared.typing import URLString
from melody.versions import python_version_info, version_info

__all__ = ("SharedHTTPClient", "Route")

KEY = "{route.method} {route.path}"
key = KEY.format


@frozen()
class Route:
    method: str
    path: str

    @property
    def key(self) -> str:
        return key(route=self)

    def with_parameters(self, **parameters: Any) -> Self:
        return evolve(self, path=self.path.format_map(parameters))


Response = Union[Payload, str, bytes]

USER_AGENT_LITERAL = "User-Agent"
USER_AGENT = f"{NAME}/{version_info} ({PYTHON}/{python_version_info})"

SESSION_NOT_ATTACHED = "`session` is not attached to the client"


@define()
class SharedHTTPClient:
    USER_AGENT: ClassVar[str] = USER_AGENT

    url: URL = field(converter=URL)
    proxy: Optional[URLString] = field(default=None, repr=False)
    proxy_auth: Optional[BasicAuth] = field(default=None, repr=False)
    timeout: float = field(default=DEFAULT_TIMEOUT)
    retries: int = field(default=DEFAULT_RETRIES)

    session_unchecked: Optional[ClientSession] = field(default=None, repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        add_client(self)

    @property
    def session(self) -> ClientSession:
        session = self.session_unchecked

        if session is None:
            raise ValueError(SESSION_NOT_ATTACHED)

        return session

    @session.setter
    def session(self, session: ClientSession) -> None:
        self.session_unchecked = session

    @session.deleter
    def session(self) -> None:
        self.session_unchecked = None

    def has_session(self) -> bool:
        return self.session_unchecked is not None

    def create_timeout(self) -> ClientTimeout:
        return ClientTimeout(total=self.timeout)

    async def close(self) -> None:
        if self.has_session():
            await self.session.close()

            del self.session

    async def create_session(self) -> ClientSession:
        return ClientSession(headers={USER_AGENT_LITERAL: self.USER_AGENT})

    async def ensure_session(self) -> ClientSession:
        if self.has_session():
            return self.session

        self.session = session = await self.create_session()

        return session

    @overload
    async def request(
        self,
        method: str,
        url: URLString,
        response_type: Literal[ResponseType.JSON] = ...,
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> Payload:
        ...

    @overload
    async def request(
        self,
        method: str,
        url: URLString,
        response_type: Literal[ResponseType.TEXT],
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> str:
        ...

    @overload
    async def request(
        self,
        method: str,
        url: URLString,
        response_type: Literal[ResponseType.BYTES],
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> bytes:
        ...

    @overload
    async def request(
        self,
        method: str,
        url: URLString,
        response_type: ResponseType,
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> Response:
        ...

    async def request(
        self,
        method: str,
        url: URLString,
        response_type: ResponseType = ResponseType.JSON,
        payload: Optional[Payload] = None,
        data: Optional[Parameters] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
        auth: Optional[BasicAuth] = None,
    ) -> Response:
        attempts = self.retries + 1

        error: Optional[ClientError] = None

        session = await self.ensure_session()

        while attempts:
            try:
                async with session.request(
                    method,
                    url,
                    params=parameters,
                    data=data,
                    json=payload,
                    headers=headers,
                    proxy=self.proxy,
                    proxy_auth=self.proxy_auth,
                    auth=auth,
                    timeout=self.create_timeout(),
                ) as response:
                    response.raise_for_status()

                    if response_type.is_json():
                        return await response.json()  # type: ignore[no-any-return]

                    if response_type.is_text():
                        return await response.text()

                    return await response.read()

            except ClientError as origin:
                error = origin

            finally:
                await sleep(ZERO)

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
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> Payload:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: Literal[ResponseType.TEXT],
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> str:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: Literal[ResponseType.BYTES],
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> bytes:
        ...

    @overload
    async def request_route(
        self,
        route: Route,
        response_type: ResponseType,
        payload: Optional[Payload] = ...,
        data: Optional[Parameters] = ...,
        parameters: Optional[Parameters] = ...,
        headers: Optional[Headers] = ...,
        auth: Optional[BasicAuth] = ...,
    ) -> Response:
        ...

    async def request_route(
        self,
        route: Route,
        response_type: ResponseType = ResponseType.JSON,
        payload: Optional[Payload] = None,
        data: Optional[Parameters] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
        auth: Optional[BasicAuth] = None,
    ) -> Response:
        return await self.request(
            route.method,
            self.url / route.path.strip(SLASH),
            response_type=response_type,
            payload=payload,
            data=data,
            parameters=parameters,
            headers=headers,
            auth=auth,
        )


CLIENTS: List[SharedHTTPClient] = []


def add_client(client: SharedHTTPClient) -> None:
    CLIENTS.append(client)


def remove_client(client: SharedHTTPClient) -> None:
    CLIENTS.remove(client)


async def close_all_clients() -> None:
    for client in CLIENTS:
        await client.close()


def close_all_clients_sync() -> None:
    run(close_all_clients())


register_at_exit(close_all_clients_sync)
