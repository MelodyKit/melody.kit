from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from melody.kit.core import app
from melody.web.constants import STATIC, STATIC_NAME, STATIC_PATH, TEMPLATES

__all__ = ("environment",)

environment = Environment(
    loader=FileSystemLoader(TEMPLATES),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True,
    enable_async=True,
)

app.mount(STATIC_PATH, StaticFiles(directory=STATIC), name=STATIC_NAME)
