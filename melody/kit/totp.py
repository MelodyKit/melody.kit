from typing import Optional
from uuid import UUID

from fastapi import Depends, Form
from pyotp import TOTP
from pyotp import random_base32 as generate_secret
from typing_extensions import Annotated
from yarl import URL

from melody.kit.contexts import UserContext
from melody.kit.core import config, database, redis
from melody.kit.errors import AuthExpectedCode, AuthInvalidCode, NotFound
from melody.kit.oauth2 import UserTokenDependency
from melody.shared.constants import IMAGE_TYPE, NAME_SEPARATOR

__all__ = (
    "generate_secret_for",
    "delete_secret_for",
    "fetch_secret_for",
    "provisioning_url",
    "secret_image_name",
    "validate_optional",
    # dependencies
    "CodeDependency",
    "OptionalCodeDependency",
    "TwoFactorTokenDependency",
    "two_factor_token_dependency",
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


CODE_MISMATCH = "code mismatch"
EXPECTED_CODE = "expected code"


def validate_optional(secret: Optional[str], code: Optional[str]) -> None:
    if secret is None:
        return

    if code is None:
        raise AuthExpectedCode(EXPECTED_CODE)

    totp = TOTP(secret)

    if not totp.verify(code):
        raise AuthInvalidCode(CODE_MISMATCH)


CodeDependency = Annotated[str, Form()]
OptionalCodeDependency = Annotated[Optional[str], Form()]


CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format


async def two_factor_token_dependency(
    context: UserTokenDependency, code: OptionalCodeDependency = None
) -> UserContext:
    self_id = context.user_id

    self_info = await database.query_user_info(user_id=self_id)

    if self_info is None:
        raise NotFound(can_not_find_user(self_id))

    validate_optional(self_info.secret, code)

    return context


TwoFactorTokenDependency = Annotated[UserContext, Depends(two_factor_token_dependency)]
