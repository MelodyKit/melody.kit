import click

from melody.bot.core import client
from melody.kit.core import config

__all__ = ("bot",)


@click.option("--token", "-t", type=str, default=config.bot.token)
@click.command()
def bot(token: str) -> None:
    client.run(token)
