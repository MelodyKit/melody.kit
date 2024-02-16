from secrets import token_hex

from melody.kit.core import config

__all__ = ("generate_secret",)


def generate_secret() -> str:
    return token_hex(config.secret.size)
