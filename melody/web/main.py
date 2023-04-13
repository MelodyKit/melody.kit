from pathlib import Path
from subprocess import call
from sys import exit
from typing import Sequence

import click

from melody.kit.main import run
from melody.web.constants import DEFAULT_INPUT, DEFAULT_OUTPUT, DEFAULT_WATCH, WEB_ROOT

EXECUTE = "npx"
TAILWIND = "tailwindcss"
INPUT = "-i"
OUTPUT = "-o"
MINIFY = "-m"
WATCH = "-w"


def build_command(input: Path, output: Path, watch: bool) -> Sequence[str]:
    arguments = [EXECUTE, TAILWIND, INPUT, input.as_posix(), OUTPUT, output.as_posix(), MINIFY]

    if watch:
        arguments.append(WATCH)

    return arguments


@click.group()
def web() -> None:
    pass


web.add_command(run)


SHELL = True


@click.option("--input", "-i", type=Path, default=DEFAULT_INPUT)
@click.option("--output", "-o", type=Path, default=DEFAULT_OUTPUT)
@click.option("--watch", "-w", is_flag=True, default=DEFAULT_WATCH)
@web.command()
def build(input: Path, output: Path, watch: bool) -> None:
    exit(call(build_command(input, output, watch=watch), cwd=WEB_ROOT, shell=SHELL))
