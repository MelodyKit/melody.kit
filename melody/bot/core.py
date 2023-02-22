from discord import Client, Intents
from discord.app_commands import CommandTree

__all__ = ("Melody", "client")

INTENTS = Intents.default()


class Melody(Client):
    def __init__(self) -> None:
        super().__init__(intents=INTENTS)

        self.synced = False

        self.tree = CommandTree(self)

    def is_synced(self) -> bool:
        return self.synced

    async def on_ready(self) -> None:
        await self.wait_until_ready()

        if not self.is_synced():
            await self.tree.sync()

            self.synced = True


client = Melody()
