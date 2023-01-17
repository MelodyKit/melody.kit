from fastapi.applications import FastAPI

from melody.kit.constants import NAME, V1, VERSION_1
from melody.kit.database import Database

__all__ = ("database", "app", "v1")

database = Database()

app = FastAPI(openapi_url=None, redoc_url=None)

v1 = FastAPI(title=NAME, version=VERSION_1)

app.mount(V1, v1)
