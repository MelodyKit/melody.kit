from secrets import token_hex

from pendulum import Duration

from melody.kit.core import config

__all__ = ("verification_code_factory", "verification_expires_in_factory")


def verification_code_factory() -> str:
    return token_hex(config.verification.size)


def verification_expires_in_factory() -> Duration:
    return config.verification.expires.duration
