from typing import Optional
from uuid import UUID

from pyotp import random_base32 as generate_secret

from melody.kit.core import redis
from melody.kit.totp.keys import secret_key

__all__ = ("generate_secret_for", "delete_secret_for", "fetch_secret_for")


async def generate_secret_for(user_id: UUID) -> str:
    secret = generate_secret()

    await redis.set(secret_key(user_id), secret)

    return secret


async def delete_secret_for(user_id: UUID) -> None:
    await redis.delete(secret_key(user_id))


async def fetch_secret_for(user_id: UUID) -> Optional[str]:
    secret = await redis.get(secret_key(user_id))

    return secret
