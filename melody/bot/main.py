import click

from melody.bot.core import client
from melody.kit.core import keyring

__all__ = ("bot",)


@click.option("--token", "-t", type=str, default=keyring.bot)
@click.command()
def bot(token: str) -> None:
    client.run(token)
