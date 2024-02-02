from enum import Enum

__all__ = ("ResponseType", "GrantType")


class ResponseType(Enum):
    BYTES = "bytes"
    TEXT = "text"
    JSON = "json"

    def is_bytes(self) -> bool:
        return self is type(self).BYTES

    def is_text(self) -> bool:
        return self is type(self).TEXT

    def is_json(self) -> bool:
        return self is type(self).JSON


class GrantType(Enum):
    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"
    REFRESH_TOKEN = "refresh_token"

    def is_authorization_code(self) -> bool:
        return self is type(self).AUTHORIZATION_CODE

    def is_client_credentials(self) -> bool:
        return self is type(self).CLIENT_CREDENTIALS

    def is_refresh_token(self) -> bool:
        return self is type(self).REFRESH_TOKEN
