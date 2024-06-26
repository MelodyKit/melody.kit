from uuid import UUID

from discord import Interaction
from discord.app_commands import Transform, Transformer

from melody.bot.core import Melody

__all__ = ("UUIDTransformer", "UUIDTransform")


class UUIDTransformer(Transformer):
    async def transform(  # type: ignore[override]
        self, interaction: Interaction[Melody], value: str
    ) -> UUID:
        return UUID(value)


UUIDTransform = Transform[UUID, UUIDTransformer]
