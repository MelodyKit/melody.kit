from typing import Optional
from uuid import UUID
from uuid import uuid4 as generate_uuid

from yarl import URL

from melody.kit.core import config, redis
from melody.kit.enums import Connection
from melody.shared.constants import NAME_SEPARATOR

__all__ = (
    "redirect_url",
    "callback_url",
    "generate_state",
    "generate_state_for",
    "delete_state",
    "fetch_user_id_by_state",
)

REDIRECT = "https://{config.domain}/api/v1/me/connections/{connection}"
redirect = REDIRECT.format

CALLBACK = "https://{config.domain}/api/v1/me/connections/{connection}/callback"
callback = CALLBACK.format

KEY = f"{{connection}}{NAME_SEPARATOR}{{state}}"
key = KEY.format


def generate_key(connection: Connection, state: str) -> str:
    return key(connection=connection.value, state=state)


def generate_state() -> str:
    return str(generate_uuid())


def redirect_url(connection: Connection) -> URL:
    return URL(redirect(config=config, connection=connection.value))


def callback_url(connection: Connection) -> URL:
    return URL(callback(config=config, connection=connection.value))


async def generate_state_for(connection: Connection, user_id: UUID) -> str:
    state = generate_state()

    await redis.set(generate_key(connection, state), str(user_id))

    return state


async def delete_state(connection: Connection, state: str) -> None:
    await redis.delete(generate_key(connection, state))


async def fetch_user_id_by_state(connection: Connection, state: str) -> Optional[UUID]:
    option = await redis.get(generate_key(connection, state))

    return None if option is None else UUID(option)
