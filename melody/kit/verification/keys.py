from typing import Optional

from melody.shared.constants import NAME_SEPARATOR, VERIFICATION_CODE

__all__ = ("verification_code_key", "key_verification_code")

VERIFICATION_CODE_KEY = f"{VERIFICATION_CODE}{NAME_SEPARATOR}{{}}"
verification_code_key = VERIFICATION_CODE_KEY.format


def key_verification_code(key: str) -> Optional[str]:
    _, _, verification_code = key.partition(NAME_SEPARATOR)

    return verification_code if verification_code else None
