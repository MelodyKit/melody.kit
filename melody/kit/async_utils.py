from functools import partial
from typing import Callable, TypeVar

from anyio.to_thread import run_sync as standard_run_blocking
from typing_extensions import ParamSpec

__all__ = ("run_blocking",)

P = ParamSpec("P")

T = TypeVar("T")


async def run_blocking(function: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return await standard_run_blocking(partial(function, *args, **kwargs))
