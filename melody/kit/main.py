import click
import uvicorn

from melody.kit.constants import DEFAULT_HOST, DEFAULT_PORT
from melody.kit.core import app

__all__ = ("kit",)


@click.option("--host", "-h", default=DEFAULT_HOST, type=str)
@click.option("--port", "-p", default=DEFAULT_PORT, type=int)
@click.command()
def kit(host: str, port: int) -> None:
    uvicorn.run(app, host=host, port=port)
