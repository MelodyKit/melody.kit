from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import RedirectResponse

from melody.discord.authorization import authorize_url
from melody.discord.client import Client
from melody.kit.connections import delete_state, fetch_user_id_by_state, generate_state_for
from melody.kit.core import database, v1
from melody.kit.dependencies import access_token_dependency
from melody.kit.enums import Connection
from melody.kit.errors import Unauthorized

USER_ID_NOT_FOUND = "can not find user ID for state `{}`"
user_id_not_found = USER_ID_NOT_FOUND.format


@v1.get("/me/connections/discord")
async def connect_discord(user_id: UUID = Depends(access_token_dependency)) -> RedirectResponse:
    state = await generate_state_for(Connection.DISCORD, user_id)

    return RedirectResponse(str(authorize_url(state)), status_code=status.HTTP_302_FOUND)


@v1.get("/me/connections/discord/callback")
async def discord_callback(code: str, state: str) -> None:
    user_id = await fetch_user_id_by_state(Connection.DISCORD, state)

    if user_id is None:
        raise Unauthorized(user_id_not_found(state))

    await delete_state(Connection.DISCORD, state)

    client = Client()

    tokens = await client.get_tokens(code=code)

    client.attach_tokens(tokens)

    entity = await client.get_self()

    await database.connect_discord(user_id, entity.id)
