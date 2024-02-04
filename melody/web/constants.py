from pathlib import Path

# constants

WEB_ROOT = Path(__file__).parent

STATIC_PATH = "/static"

CSS_NAME = "css"
KEYS_NAME = "keys"
STATIC_NAME = "static"
TEMPLATES_NAME = "templates"

KEY_SUFFIX = ".key"

KEYS = WEB_ROOT / KEYS_NAME
STATIC = WEB_ROOT / STATIC_NAME
TEMPLATES = WEB_ROOT / TEMPLATES_NAME
