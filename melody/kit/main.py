import click
import uvicorn

from melody.kit.core import app, config

__all__ = ("run",)


@click.option("--host", "-h", default=config.kit.host, type=str)
@click.option("--port", "-p", default=config.kit.port, type=int)
@click.command()
def run(host: str, port: int) -> None:
    uvicorn.run(app, host=host, port=port)
