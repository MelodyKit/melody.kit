from asyncio import get_running_loop
from types import TracebackType as Traceback
from typing import (
    IO,
    AnyStr,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    final,
)

from attrs import frozen
from typing_aliases import AnyError, AsyncCallable, Nullary, Unary
from typing_extensions import ParamSpec, Self

__all__ = (
    "run_blocking",
    "run_blocking_factory",
    "AsyncFile",
    "async_open",
    "wrap_file",
)

P = ParamSpec("P")
T = TypeVar("T")


async def run_blocking(function: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return await get_running_loop().run_in_executor(None, call_function(function, *args, **kwargs))


def call_function(function: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Nullary[T]:
    def call() -> T:
        return function(*args, **kwargs)

    return call


def run_blocking_factory(function: Callable[P, T]) -> AsyncCallable[P, T]:
    async def run(*args: P.args, **kwargs: P.kwargs) -> T:
        return await run_blocking(function, *args, **kwargs)

    return run


R = TypeVar("R")


def async_compose(outer: Unary[T, R], inner: AsyncCallable[P, T]) -> AsyncCallable[P, R]:
    async def composed(*args: P.args, **kwargs: P.kwargs) -> R:
        return outer(await inner(*args, **kwargs))

    return composed


E = TypeVar("E", bound=AnyError)

ALL = -1


@final
@frozen()
class AsyncFile(Generic[AnyStr]):
    file: IO[AnyStr]

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        error_type: Optional[Type[E]],
        error: Optional[E],
        traceback: Optional[Traceback],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await run_blocking(self.file.close)

    async def read(self, size: int = ALL) -> AnyStr:
        return await run_blocking(self.file.read, size)

    async def write(self, data: AnyStr) -> int:
        return await run_blocking(self.file.write, data)


async_open = run_blocking_factory(open)


def wrap_file(file: IO[AnyStr]) -> AsyncFile[AnyStr]:
    return AsyncFile(file)


open_file = async_compose(wrap_file, async_open)
