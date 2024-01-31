from uuid import UUID

from authlib.integrations.starlette_client import OAuthError  # type: ignore[import-untyped]
from edgedb import ConstraintViolationError
from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from melody.discord.client import Client
from melody.kit.core import database, oauth, v1
from melody.kit.dependencies import access_token_dependency
from melody.kit.errors import Conflict, InternalError
from melody.kit.tags import CONNECTIONS
from melody.shared.tokens import Tokens

USER_ID_NOT_FOUND = "can not find user ID for state `{}`"
user_id_not_found = USER_ID_NOT_FOUND.format

USER_ID = "user_id"

DISCORD_CALLBACK = "discord_callback"


@v1.get("/me/connections/discord", tags=[CONNECTIONS])
async def connect_discord(
    request: Request, user_id: UUID = Depends(access_token_dependency)
) -> RedirectResponse:
    callback_url = request.url_for(DISCORD_CALLBACK)

    request.session[USER_ID] = str(user_id)

    return await oauth.discord.authorize_redirect(  # type: ignore[no-any-return]
        request, callback_url
    )


@v1.delete("/me/connections/discord", tags=[CONNECTIONS])
async def disconnect_discord(user_id: UUID = Depends(access_token_dependency)) -> None:
    await database.update_user_discord_id(user_id=user_id, discord_id=None)


DISCORD_ID_CONNECTED = "discord ID `{}` is already connected"
discord_id_connected = DISCORD_ID_CONNECTED.format

OAUTH_ERROR = "oauth error"


@v1.get("/me/connections/discord/callback", tags=[CONNECTIONS])
async def discord_callback(request: Request) -> None:
    try:
        data = await oauth.discord.authorize_access_token(request)

    except OAuthError:
        raise InternalError(OAUTH_ERROR) from None

    tokens = Tokens.from_data(data)

    client = Client().attach_tokens(tokens)

    entity = await client.get_self()

    discord_id = str(entity.id)

    user_id = UUID(request.session.pop(USER_ID))

    try:
        await database.update_user_discord_id(user_id=user_id, discord_id=discord_id)

    except ConstraintViolationError:
        raise Conflict(discord_id_connected(discord_id)) from None
