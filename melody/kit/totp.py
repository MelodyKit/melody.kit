from typing import Optional
from uuid import UUID

from pyotp import TOTP
from pyotp import random_base32 as generate_secret
from yarl import URL

from melody.kit.core import config, redis
from melody.shared.constants import IMAGE_TYPE, NAME_SEPARATOR

__all__ = (
    "generate_secret_for",
    "delete_secret_for",
    "fetch_secret_for",
    "provisioning_url",
    "secret_image_name",
)

SECRET = "secret"

SECRET_KEY = f"{SECRET}{NAME_SEPARATOR}{{}}"
secret_key = SECRET_KEY.format


async def generate_secret_for(user_id: UUID) -> str:
    secret = generate_secret()

    await redis.set(secret_key(user_id), secret)

    return secret


async def delete_secret_for(user_id: UUID) -> None:
    await redis.delete(secret_key(user_id))


async def fetch_secret_for(user_id: UUID) -> Optional[str]:
    secret = await redis.get(secret_key(user_id))

    return secret


def provisioning_url(user_id: UUID, secret: str) -> URL:
    totp = TOTP(secret)

    uri = totp.provisioning_uri(name=str(user_id), issuer_name=config.name)

    url = URL(uri)

    return url


SECRET_IMAGE_NAME = f"{SECRET}.{{}}.{IMAGE_TYPE}"
secret_image_name = SECRET_IMAGE_NAME.format
