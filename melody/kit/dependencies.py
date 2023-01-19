from typing import Optional
from uuid import UUID

from fastapi.requests import Request
from jwt import DecodeError, ExpiredSignatureError

from melody.kit.constants import SPACE
from melody.kit.errors import AuthenticationError, ErrorCode
from melody.kit.tokens import decode_token

__all__ = ("token_dependency",)

AUTHORIZATION = "Authorization"

AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_EXPIRED = "authentication has expired"


def token_dependency(request: Request, token: Optional[str] = None) -> UUID:
    if token is None:
        header = request.headers.get(AUTHORIZATION)

        if header is None:
            raise AuthenticationError(AUTHENTICATION_MISSING, ErrorCode.AUTHENTICATION_MISSING)

        _, _, token = header.partition(SPACE)

        if not token:
            raise AuthenticationError(AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID)

    try:
        user_id = decode_token(token)

    except (DecodeError, KeyError, ValueError):
        raise AuthenticationError(
            AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID
        ) from None

    except ExpiredSignatureError:
        raise AuthenticationError(
            AUTHENTICATION_EXPIRED, ErrorCode.AUTHENTICATION_EXPIRED
        ) from None

    return user_id
