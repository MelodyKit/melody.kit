from uuid import UUID

from jwt import decode, encode
from typing_extensions import TypedDict

from melody.kit.core import config
from melody.kit.utils import utc_now

__all__ = ("TokenData", "encode_token", "decode_token")


class TokenData(TypedDict):
    token: str


ALGORITHM = "HS256"

CREATED_AT = "iat"
# EXPIRES_AT = "exp"
SUBJECT = "sub"


def encode_token(user_id: UUID) -> str:
    created_at = utc_now()

    # expires_at = ...

    payload = {
        CREATED_AT: created_at.int_timestamp,
        # EXPIRES_AT: expires_at.int_timestamp,
        SUBJECT: str(user_id),
    }

    return encode(payload, config.kit.key, algorithm=ALGORITHM)


def decode_token(token: str) -> UUID:
    payload = decode(token, config.kit.key, algorithms=[ALGORITHM])

    string = payload[SUBJECT]

    return UUID(string)
