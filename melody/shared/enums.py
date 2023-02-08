from enum import Enum

__all__ = ("ResponseType",)


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
