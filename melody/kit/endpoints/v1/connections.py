from uuid import UUID

from authlib.integrations.starlette_client import OAuthError  # type: ignore[import-untyped]
from edgedb import ConstraintViolationError
from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from yarl import URL

from melody.discord.client import Client
from melody.kit.core import database, oauth, v1
from melody.kit.dependencies import access_token_dependency, url_dependency
from melody.kit.errors import InternalError

USER_ID_NOT_FOUND = "can not find user ID for state `{}`"
user_id_not_found = USER_ID_NOT_FOUND.format

DISCORD_CALLBACK = "discord_callback"


@v1.get("/me/connections/discord", dependencies=[Depends(access_token_dependency)])
async def connect_discord(request: Request) -> RedirectResponse:
    redirect_url = request.url_for(DISCORD_CALLBACK)

    return await oauth.discord.authorize_redirect(  # type: ignore[no-any-return]
        request, redirect_url
    )


@v1.delete("/me/connections/discord")
async def disconnect_discord(user_id: UUID = Depends(access_token_dependency)) -> None:
    await database.update_user_discord_id(user_id=user_id, discord_id=None)


DISCORD_ID_CONNECTED = "discord ID `{}` is already connected"
discord_id_connected = DISCORD_ID_CONNECTED.format

OAUTH_ERROR = "oauth error"


@v1.get("/me/connections/discord/callback")
async def discord_callback(request: Request) -> None:
    try:
        token = await oauth.discord.authorize_access_token(request)

    except OAuthError:
        raise InternalError(OAUTH_ERROR) from None

    print(token)
