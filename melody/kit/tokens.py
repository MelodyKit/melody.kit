from uuid import UUID

from jwt import ExpiredSignatureError, decode, encode
from typing_extensions import TypedDict as Data

from melody.kit.core import config, tokens
from melody.shared.date_time import utc_from_timestamp, utc_now

__all__ = ("TokenData", "encode_token", "decode_token")


class TokenData(Data):
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


EXPIRED_TOKEN = "token has expired"


def decode_token(token: str) -> UUID:
    payload = decode(token, config.kit.key, algorithms=[ALGORITHM])

    created_at = utc_from_timestamp(payload[CREATED_AT])

    string = payload[SUBJECT]

    user_id = UUID(string)

    if user_id in tokens:
        if tokens[user_id] > created_at:
            raise ExpiredSignatureError(EXPIRED_TOKEN)

    return user_id
