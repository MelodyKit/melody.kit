import click
import uvicorn

from melody.kit.core import app, config
from melody.kit.enums import LogLevel

__all__ = ("run",)


@click.option("--host", "-h", default=config.kit.host, type=str)
@click.option("--port", "-p", default=config.kit.port, type=int)
@click.option("--log-level", "-l", default=config.log.level, type=LogLevel)
@click.command()
def run(host: str, port: int, log_level: LogLevel) -> None:
    uvicorn.run(app, host=host, port=port, log_level=log_level.value)
