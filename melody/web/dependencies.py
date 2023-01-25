from typing import Optional
from uuid import UUID

from fastapi.requests import Request
from jwt import DecodeError, ExpiredSignatureError

from melody.kit.errors import AuthenticationError, ErrorCode
from melody.kit.tokens import decode_token
from melody.web.constants import TOKEN

__all__ = ("cookie_token_dependency", "optional_cookie_token_dependency")

AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_EXPIRED = "authentication has expired"


def cookie_token_dependency(request: Request) -> UUID:
    cookies = request.cookies

    token = cookies.get(TOKEN)

    if token is None:
        raise AuthenticationError(AUTHENTICATION_MISSING, ErrorCode.AUTHENTICATION_MISSING)

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


def optional_cookie_token_dependency(request: Request) -> Optional[UUID]:
    try:
        return cookie_token_dependency(request)

    except AuthenticationError:
        return None
