from typing import Optional

from fastapi import Depends, Form, Security
from fastapi.security import SecurityScopes
from typing_extensions import Annotated

from melody.kit.errors.auth import (
    AuthAccessTokenExpectedUser,
    AuthAccessTokenExpectedUserBased,
    AuthAccessTokenInvalid,
    AuthAccessTokenScopesMissing,
    AuthRefreshTokenInvalid,
)
from melody.kit.scopes import (
    USER_FOLLOWING_READ,
    USER_FOLLOWING_WRITE,
    USER_IMAGE_READ,
    USER_IMAGE_WRITE,
    USER_LIBRARY_READ,
    USER_LIBRARY_WRITE,
    USER_PLAYLISTS_READ,
    USER_PLAYLISTS_WRITE,
    USER_SETTINGS_READ,
    USER_SETTINGS_WRITE,
    USER_STREAMS_READ,
    USER_STREAMS_WRITE,
)
from melody.kit.tokens.context import (
    BoundToken,
    Context,
    UserBasedContext,
    UserContext,
    is_client_user_context,
    is_user_context,
)
from melody.kit.tokens.operations import (
    fetch_context_by_access_token,
    fetch_context_by_refresh_token,
)
from melody.kit.tokens.scheme import oauth2_scheme
from melody.shared.tokens import Scopes

__all__ = (
    # user access tokens
    "BoundUserTokenDependency",
    "UserTokenDependency",
    "bound_user_token_dependency",
    "user_token_dependency",
    # user-based access tokens
    "BoundUserBasedTokenDependency",
    "UserBasedTokenDependency",
    "bound_user_based_token_dependency",
    "user_based_token_dependency",
    # scoped access tokens
    "FollowingReadTokenDependency",
    "FollowingWriteTokenDependency",
    "LibraryReadTokenDependency",
    "LibraryWriteTokenDependency",
    "PlaylistsReadTokenDependency",
    "PlaylistsWriteTokenDependency",
    "SettingsReadTokenDependency",
    "SettingsWriteTokenDependency",
    "ImageReadTokenDependency",
    "ImageWriteTokenDependency",
    "StreamsReadTokenDependency",
    "StreamsWriteTokenDependency",
    # general access tokens
    "BoundTokenDependency",
    "TokenDependency",
    "bound_token_dependency",
    "token_dependency",
    # refresh tokens
    "BoundRefreshTokenDependency",
    "OptionalBoundRefreshTokenDependency",
    "bound_refresh_token_dependency",
    "optional_bound_refresh_token_dependency",
)

OAuth2SchemeTokenDependency = Annotated[str, Depends(oauth2_scheme)]


async def bound_user_token_dependency(
    token: OAuth2SchemeTokenDependency,
) -> BoundToken[UserContext]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthAccessTokenInvalid()

    if is_user_context(context):
        return BoundToken(token, context)

    raise AuthAccessTokenExpectedUser()


BoundUserTokenDependency = Annotated[BoundToken[UserContext], Depends(bound_user_token_dependency)]


async def user_token_dependency(bound_user_token: BoundUserTokenDependency) -> UserContext:
    return bound_user_token.context


UserTokenDependency = Annotated[UserContext, Depends(user_token_dependency)]


async def bound_user_based_token_dependency(
    security_scopes: SecurityScopes, token: OAuth2SchemeTokenDependency
) -> BoundToken[UserBasedContext]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthAccessTokenInvalid()

    if is_user_context(context):
        return BoundToken(token, context)

    scopes = frozenset(security_scopes.scopes)

    if is_client_user_context(context):
        missing = scopes.difference(context.scopes.tokens)

        if missing:
            missing_scopes = Scopes(missing)

            raise AuthAccessTokenScopesMissing(missing_scopes)

        return BoundToken(token, context)

    raise AuthAccessTokenExpectedUserBased()


BoundUserBasedTokenDependency = Annotated[
    BoundToken[UserBasedContext], Depends(bound_user_based_token_dependency)
]


async def user_based_token_dependency(
    bound_user_based_token: BoundUserBasedTokenDependency,
) -> UserBasedContext:
    return bound_user_based_token.context


UserBasedTokenDependency = Annotated[UserBasedContext, Depends(user_based_token_dependency)]


FollowingReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_FOLLOWING_READ])
]
FollowingWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_FOLLOWING_WRITE])
]
LibraryReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_LIBRARY_READ])
]
LibraryWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_LIBRARY_WRITE])
]
PlaylistsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_PLAYLISTS_READ])
]
PlaylistsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_PLAYLISTS_WRITE])
]
SettingsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_SETTINGS_READ])
]
SettingsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_SETTINGS_WRITE])
]
ImageReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_IMAGE_READ])
]
ImageWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_IMAGE_WRITE])
]
StreamsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_STREAMS_READ])
]
StreamsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_STREAMS_WRITE])
]


async def bound_token_dependency(token: OAuth2SchemeTokenDependency) -> BoundToken[Context]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthAccessTokenInvalid()

    return BoundToken(token, context)


BoundTokenDependency = Annotated[BoundToken[Context], Depends(bound_token_dependency)]


async def token_dependency(bound_token: BoundTokenDependency) -> Context:
    return bound_token.context


TokenDependency = Annotated[Context, Depends(token_dependency)]


FormRefreshTokenDependency = Annotated[str, Form()]
OptionalFormRefreshTokenDependency = Annotated[Optional[str], Form()]


async def bound_refresh_token_dependency(
    refresh_token: FormRefreshTokenDependency,
) -> BoundToken[Context]:
    context = await fetch_context_by_refresh_token(refresh_token)

    if context is None:
        raise AuthRefreshTokenInvalid()

    return BoundToken(refresh_token, context)


BoundRefreshTokenDependency = Annotated[
    BoundToken[Context], Depends(bound_refresh_token_dependency)
]


async def optional_bound_refresh_token_dependency(
    refresh_token: OptionalFormRefreshTokenDependency = None,
) -> Optional[BoundToken[Context]]:
    return None if refresh_token is None else await bound_refresh_token_dependency(refresh_token)


OptionalBoundRefreshTokenDependency = Annotated[
    Optional[BoundToken[Context]], Depends(optional_bound_refresh_token_dependency)
]
