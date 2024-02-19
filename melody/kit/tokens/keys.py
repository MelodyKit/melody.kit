from typing import Optional

from melody.shared.constants import ACCESS_TOKEN, NAME_SEPARATOR, REFRESH_TOKEN

__all__ = (
    "access_token_key",
    "key_access_token",
    "refresh_token_key",
    "key_refresh_token",
)

ACCESS_TOKEN_KEY = f"{ACCESS_TOKEN}{NAME_SEPARATOR}{{}}"
access_token_key = ACCESS_TOKEN_KEY.format

REFRESH_TOKEN_KEY = f"{REFRESH_TOKEN}{NAME_SEPARATOR}{{}}"
refresh_token_key = REFRESH_TOKEN_KEY.format


def key_access_token(key: str) -> Optional[str]:
    _, _, access_token = key.partition(NAME_SEPARATOR)

    return access_token if access_token else None


def key_refresh_token(key: str) -> Optional[str]:
    _, _, refresh_token = key.partition(NAME_SEPARATOR)

    return refresh_token if refresh_token else None
