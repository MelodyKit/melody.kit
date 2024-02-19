from secrets import token_urlsafe as token_url_safe

from pendulum import Duration

from melody.kit.core import config

__all__ = ("authorization_code_factory", "authorization_expires_in_factory")


def authorization_code_factory() -> str:
    return token_url_safe(config.authorization.size)


def authorization_expires_in_factory() -> Duration:
    return config.authorization.expires.duration
