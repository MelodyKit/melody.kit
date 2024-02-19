from fastapi import status
from fastapi.responses import PlainTextResponse

from melody.kit.core import app
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS
from melody.web.constants import KEY_SUFFIX, KEYS

__all__ = ("get_key",)

CAN_NOT_FIND_KEY = "can not find `{}` key"
can_not_find_key = CAN_NOT_FIND_KEY.format


@app.get("/keys/{name}")
async def get_key(name: str) -> PlainTextResponse:
    path = (KEYS / name).with_suffix(KEY_SUFFIX)

    if path.exists():
        return PlainTextResponse(path.read_text(DEFAULT_ENCODING, DEFAULT_ERRORS))

    return PlainTextResponse(can_not_find_key(name), status_code=status.HTTP_404_NOT_FOUND)
