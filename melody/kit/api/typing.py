from aiohttp.web import Request, Response, StreamResponse

from typing import Any, Awaitable, Callable, TypeVar

T = TypeVar("T")

R = TypeVar("R")

Unary = Callable[[T], R]

AsyncUnary = Unary[T, Awaitable[R]]

DynamicCallable = Callable[..., R]
AnyCallable = DynamicCallable[Any]

F = TypeVar("F", bound=AnyCallable)
G = TypeVar("G", bound=AnyCallable)

Decorator = Unary[F, G]
DecoratorIdentity = Decorator[F, F]

I = TypeVar("I", bound=Request)
O = TypeVar("O", bound=StreamResponse)

GenericHandler = AsyncUnary[I, O]
Handler = GenericHandler[Request, Response]
StreamHandler = GenericHandler[Request, StreamResponse]
