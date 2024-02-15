from enum import Enum
from typing import ClassVar, Literal, Type, Union
from uuid import UUID

from attrs import frozen
from cattrs.strategies import configure_tagged_union
from typing_extensions import TypeGuard

from melody.shared.converter import CONVERTER
from melody.shared.tokens import (
    Scopes,
    register_structure_hook_rename_scopes,
    register_unstructure_hook_rename_scopes,
)
from melody.shared.typing import Data

__all__ = (
    # context types
    "ContextType",
    # contexts
    "UserContext",
    "UserContextData",
    "ClientContext",
    "ClientContextData",
    "ClientUserContext",
    "ClientUserContextData",
    # converters
    "context_from_data",
    "context_into_data",
    # type guards
    "is_user_context",
    "is_client_context",
    "is_client_user_context",
)


UserLiteral = Literal["user"]
ClientLiteral = Literal["client"]
ClientUserLiteral = Literal["client_user"]

ContextLiteral = Union[UserLiteral, ClientLiteral, ClientUserLiteral]

USER_LITERAL: UserLiteral = "user"
CLIENT_LITERAL: ClientLiteral = "client"
CLIENT_USER_LITERAL: ClientUserLiteral = "client_user"


class ContextType(Enum):
    USER = USER_LITERAL
    CLIENT = CLIENT_LITERAL
    CLIENT_USER = CLIENT_USER_LITERAL

    def is_user(self) -> bool:
        return self is type(self).USER

    def is_client(self) -> bool:
        return self is type(self).CLIENT

    def is_client_user(self) -> bool:
        return self is type(self).CLIENT_USER


UserTypeLiteral = Literal[ContextType.USER]
ClientTypeLiteral = Literal[ContextType.CLIENT]
ClientUserTypeLiteral = Literal[ContextType.CLIENT_USER]

USER_TYPE: UserTypeLiteral = ContextType.USER
CLIENT_TYPE: ClientTypeLiteral = ContextType.CLIENT
CLIENT_USER_TYPE: ClientUserTypeLiteral = ContextType.CLIENT_USER


class ContextTypeData(Data):
    context_type: ContextLiteral


class UserContextData(ContextTypeData):
    user_id: str


@frozen()
class UserContext:
    TYPE: ClassVar[UserTypeLiteral] = USER_TYPE

    user_id: UUID


class ClientContextData(ContextTypeData):
    client_id: str


@frozen()
class ClientContext:
    TYPE: ClassVar[ClientTypeLiteral] = CLIENT_TYPE

    client_id: UUID


class ClientUserContextData(ContextTypeData):
    client_id: str
    user_id: str
    scope: str


@register_unstructure_hook_rename_scopes
@register_structure_hook_rename_scopes
@frozen()
class ClientUserContext:
    TYPE: ClassVar[ClientUserTypeLiteral] = CLIENT_USER_TYPE

    client_id: UUID
    user_id: UUID
    scopes: Scopes


Context = Union[UserContext, ClientContext, ClientUserContext]
ContextData = Union[UserContextData, ClientContextData, ClientUserContextData]

UserBasedContext = Union[UserContext, ClientUserContext]
UserBasedContextData = Union[UserContextData, ClientUserContextData]


def type_of_context_type(context_type: Type[Context]) -> ContextType:
    return context_type.TYPE


def type_of_context(context: Context) -> ContextType:
    return type_of_context_type(type(context))


def literal_of_context_type(context_type: Type[Context]) -> ContextLiteral:
    return type_of_context_type(context_type).value  # type: ignore[no-any-return]


def is_user_context(context: Context) -> TypeGuard[UserContext]:
    return type_of_context(context) is USER_TYPE


def is_client_context(context: Context) -> TypeGuard[ClientContext]:
    return type_of_context(context) is CLIENT_TYPE


def is_client_user_context(context: Context) -> TypeGuard[ClientUserContext]:
    return type_of_context(context) is CLIENT_USER_TYPE


CONTEXT_TYPE = "context_type"


configure_tagged_union(Context, CONVERTER, literal_of_context_type, CONTEXT_TYPE)


def context_from_data(data: ContextData) -> Context:
    return CONVERTER.structure(data, Context)  # type: ignore[arg-type]


def context_into_data(context: Context) -> ContextData:
    return CONVERTER.unstructure(context, Context)  # type: ignore[no-any-return]
