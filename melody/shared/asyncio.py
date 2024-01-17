from asyncio import get_running_loop
from types import TracebackType as Traceback
from typing import (
    IO,
    Any,
    AnyStr,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    final,
    overload,
)

from attrs import frozen
from typing_aliases import AnyError, Nullary
from typing_extensions import ParamSpec, Self

from melody.shared.constants import (
    DEFAULT_CLOSEFD,
    DEFAULT_ENCODING,
    DEFAULT_ERRORS,
    READ,
)
from melody.shared.typing import (
    FileDescriptorOrIntoPath,
    FileOpener,
    OpenBinaryMode,
    OpenMode,
    OpenTextMode,
)

__all__ = ("run_blocking", "call_function")

P = ParamSpec("P")
T = TypeVar("T")


async def run_blocking(function: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return await get_running_loop().run_in_executor(None, call_function(function, *args, **kwargs))


def call_function(function: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Nullary[T]:
    def call() -> T:
        return function(*args, **kwargs)

    return call


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


@overload
async def open_file(
    file: FileDescriptorOrIntoPath,
    mode: OpenBinaryMode,
    buffering: int = ...,
    encoding: str = ...,
    errors: str = ...,
    closefd: bool = ...,
    opener: Optional[FileOpener] = ...,
) -> AsyncFile[bytes]:
    ...


@overload
async def open_file(
    file: FileDescriptorOrIntoPath,
    mode: OpenTextMode = ...,
    buffering: int = ...,
    encoding: str = ...,
    errors: str = ...,
    closefd: bool = ...,
    opener: Optional[FileOpener] = ...,
) -> AsyncFile[str]:
    ...


async def open_file(
    file: FileDescriptorOrIntoPath,
    mode: OpenMode = READ,
    buffering: int = ALL,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
    closefd: bool = DEFAULT_CLOSEFD,
    opener: Optional[FileOpener] = None,
) -> AsyncFile[Any]:
    result = await run_blocking(
        open,
        file,
        mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        closefd=closefd,
        opener=opener,
    )

    return wrap_file(result)


def wrap_file(file: IO[AnyStr]) -> AsyncFile[AnyStr]:
    return AsyncFile(file)
