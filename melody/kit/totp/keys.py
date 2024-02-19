from typing import Optional

from melody.shared.constants import NAME_SEPARATOR, SECRET

__all__ = ("secret_key", "key_secret")

SECRET_KEY = f"{SECRET}{NAME_SEPARATOR}{{}}"
secret_key = SECRET_KEY.format


def key_secret(key: str) -> Optional[str]:
    _, _, secret = key.partition(NAME_SEPARATOR)

    return secret if secret else None
