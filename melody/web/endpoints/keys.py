from fastapi import status
from fastapi.responses import PlainTextResponse

from melody.kit.core import app
from melody.kit.errors import Error, ErrorCode
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS
from melody.web.constants import KEY_SUFFIX, KEYS

__all__ = ("get_key",)

CAN_NOT_FIND_KEY = "can not find `{}` key"


@app.get("/keys/{name}")
async def get_key(name: str) -> PlainTextResponse:
    path = (KEYS / name).with_suffix(KEY_SUFFIX)

    if path.exists():
        return PlainTextResponse(path.read_text(DEFAULT_ENCODING, DEFAULT_ERRORS))

    raise Error(CAN_NOT_FIND_KEY.format(name), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND)
