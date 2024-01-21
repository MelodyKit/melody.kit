from random import choice

from colors import Color
from discord import Color as DiscordColor

from melody.shared.constants import MELODY_COLORS

__all__ = ("color_into_discord", "random_melody_color")


def color_into_discord(color: Color) -> DiscordColor:
    return DiscordColor(color.value)


def random_melody_color() -> Color:
    return choice(MELODY_COLORS)
