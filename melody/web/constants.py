from pathlib import Path

from typing_extensions import Literal

# constants

WEB_ROOT = Path(__file__).parent

NEW_LINE = "\n"
BREAK = "<br>"

TOKEN: Literal["token"] = "token"

STATIC_PATH = "/static"

CSS_NAME = "css"
KEYS_NAME = "keys"
STATIC_NAME = "static"
TEMPLATES_NAME = "templates"

KEY_SUFFIX = ".key"

KEYS = WEB_ROOT / KEYS_NAME
STATIC = WEB_ROOT / STATIC_NAME
TEMPLATES = WEB_ROOT / TEMPLATES_NAME

CSS = STATIC / CSS_NAME

# defaults

DEFAULT_INPUT_NAME = "input.css"
DEFAULT_OUTPUT_NAME = "output.css"

DEFAULT_INPUT = CSS / DEFAULT_INPUT_NAME
DEFAULT_OUTPUT = CSS / DEFAULT_OUTPUT_NAME

DEFAULT_WATCH = False
