from colors import Color
from discord import Embed

from melody.bot.colors import color_into_discord

__all__ = ("error_embed", "not_found_embed")

ERROR_COLOR = Color(0xFF0000)

NOT_FOUND = "Not Found"


def error_embed(title: str, description: str) -> Embed:
    return Embed(color=color_into_discord(ERROR_COLOR), title=title, description=description)


def not_found_embed(description: str) -> Embed:
    return error_embed(NOT_FOUND, description)
