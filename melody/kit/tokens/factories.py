from secrets import token_hex

from pendulum import Duration

from melody.kit.core import config

__all__ = (
    "access_token_factory",
    "expires_in_factory",
    "token_type_factory",
    "refresh_token_factory",
    "refresh_expires_in_factory",
)


def access_token_factory() -> str:
    return token_hex(config.token.access.size)


def expires_in_factory() -> Duration:
    return config.token.access.expires.duration


def token_type_factory() -> str:
    return config.token.type


def refresh_token_factory() -> str:
    return token_hex(config.token.refresh.size)


def refresh_expires_in_factory() -> Duration:
    return config.token.refresh.expires.duration
