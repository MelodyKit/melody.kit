from typing import Optional

from melody.shared.constants import AUTHORIZATION_CODE, NAME_SEPARATOR

__all__ = ("authorization_code_key", "key_authorization_code")

AUTHORIZATION_CODE_KEY = f"{AUTHORIZATION_CODE}{NAME_SEPARATOR}{{}}"
authorization_code_key = AUTHORIZATION_CODE_KEY.format


def key_authorization_code(key: str) -> Optional[str]:
    _, _, authorization_code = key.partition(NAME_SEPARATOR)

    return authorization_code if authorization_code else None
