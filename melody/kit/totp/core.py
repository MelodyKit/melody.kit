from typing import Optional

from pyotp import TOTP

from melody.kit.core import config
from melody.kit.errors.auth import AuthCodeExpected, AuthCodeMismatch

__all__ = ("create_totp", "validate_totp")


def create_totp(secret: str) -> TOTP:
    totp_config = config.totp

    totp = TOTP(
        secret, digits=totp_config.digits, interval=totp_config.interval, issuer=config.name
    )

    return totp


def validate_totp(secret: Optional[str], code: Optional[str]) -> None:
    if secret is None:
        return  # TOTP not enabled

    if code is None:
        raise AuthCodeExpected()

    totp = create_totp(secret)

    if not totp.verify(code, valid_window=config.totp.valid_window):
        raise AuthCodeMismatch()
