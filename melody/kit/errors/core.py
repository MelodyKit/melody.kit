from __future__ import annotations

from enum import Enum
from typing import ClassVar, Optional, Type

from fastapi import status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as HTTPError
from typing_aliases import NormalError
from typing_extensions import Self

from melody.shared.strings import case_fold
from melody.shared.typing import Data

__all__ = ("ErrorCode", "Error", "ErrorData", "ErrorType")

VALIDATION_ERROR = "validation error"


class ErrorCode(Enum):
    BASE = 10000

    BAD_REQUEST = 10400
    UNAUTHORIZED = 10401
    FORBIDDEN = 10403
    NOT_FOUND = 10404
    METHOD_NOT_ALLOWED = 10405
    CONFLICT = 10409
    GONE = 10410
    PAYLOAD_TOO_LARGE = 10413
    UNPROCESSABLE_ENTITY = 10422
    TOO_MANY_REQUESTS = 10429

    INTERNAL_SERVER_ERROR = 10500

    DEFAULT = 13000

    ALBUM_ERROR = 13100
    ALBUM_NOT_FOUND = 13001

    ARTIST_ERROR = 13200
    ARTIST_NOT_FOUND = 13201

    TRACK_ERROR = 13300
    TRACK_NOT_FOUND = 13301

    PLAYLIST_ERROR = 13400
    PLAYLIST_NOT_FOUND = 13401
    PLAYLIST_INACCESSIBLE = 13402
    PLAYLIST_IMAGE_NOT_FOUND = 13403

    USER_ERROR = 13500
    USER_NOT_FOUND = 13501
    USER_INACCESSIBLE = 13502
    USER_IMAGE_NOT_FOUND = 13503
    USER_FOLLOW_SELF_FORBIDDEN = 13504
    USER_FOLLOW_SELF_PLAYLISTS_FORBIDDEN = 13505

    CLIENT_ERROR = 13600
    CLIENT_NOT_FOUND = 13601
    CLIENT_INACCESSIBLE = 13602

    STREAM_ERROR = 13700
    STREAM_NOT_FOUND = 13701
    STREAM_INACCESSIBLE = 13702

    AUTH_ERROR = 13800

    AUTH_ACCESS_TOKEN_ERROR = 13810
    AUTH_ACCESS_TOKEN_EXPECTED = 13811
    AUTH_ACCESS_TOKEN_INVALID = 13812
    AUTH_ACCESS_TOKEN_EXPECTED_TYPE = 13813
    AUTH_ACCESS_TOKEN_EXPECTED_USER = 13814
    AUTH_ACCESS_TOKEN_EXPECTED_USER_BASED = 13815
    AUTH_ACCESS_TOKEN_SCOPES_MISSING = 13816

    AUTH_REFRESH_TOKEN_ERROR = 13820
    AUTH_REFRESH_TOKEN_EXPECTED = 13821
    AUTH_REFRESH_TOKEN_INVALID = 13822

    AUTH_CLIENT_CREDENTIALS_ERROR = 13830
    AUTH_CLIENT_CREDENTIALS_EXPECTED = 13831
    AUTH_CLIENT_CREDENTIALS_INVALID = 13832
    AUTH_CLIENT_CREDENTIALS_MISMATCH = 13833
    AUTH_CLIENT_CREDENTIALS_NOT_FOUND = 13834
    AUTH_CLIENT_CREDENTIALS_SECRET_MISMATCH = 13835

    AUTH_AUTHORIZATION_CODE_ERROR = 13840
    AUTH_AUTHORIZATION_CODE_EXPECTED = 13841
    AUTH_AUTHORIZATION_CODE_INVALID = 13842
    AUTH_AUTHORIZATION_CODE_REDIRECT_URI_EXPECTED = 13843
    AUTH_AUTHORIZATION_CODE_REDIRECT_URI_MISMATCH = 13844

    AUTH_VERIFICATION_CODE_ERROR = 13850
    AUTH_VERIFICATION_CODE_INVALID = 13851

    AUTH_EMAIL_ERROR = 13860
    AUTH_EMAIL_INVALID = 13861
    AUTH_EMAIL_CONFLICT = 13862
    AUTH_EMAIL_FAILED = 13863
    AUTH_EMAIL_NOT_FOUND = 13864

    AUTH_PASSWORD_ERROR = 13870
    AUTH_PASSWORD_INVALID = 13871
    AUTH_PASSWORD_MISMATCH = 13872

    AUTH_CODE_ERROR = 13880
    AUTH_CODE_EXPECTED = 13881
    AUTH_CODE_MISMATCH = 13882
    AUTH_CODE_CONFLICT = 13883
    AUTH_CODE_NOT_FOUND = 13884

    AUTH_USER_ERROR = 13890
    AUTH_USER_NOT_FOUND = 13891
    AUTH_USER_UNVERIFIED = 13892

    IMAGE_ERROR = 13900
    IMAGE_UNEXPECTED_TYPE = 13901
    IMAGE_EXPECTED_SQUARE = 13902
    IMAGE_TOO_LARGE = 13903

    VALIDATION_ERROR = 14000

    @classmethod
    def from_status_code(cls, status_code: int) -> ErrorCode:
        base = cls.BASE

        try:
            return cls(base.value + status_code)

        except ValueError:
            return base


class ErrorData(Data):
    code: int
    message: str


class Error(NormalError):
    DEFAULT_CODE: ClassVar[ErrorCode]
    DEFAULT_STATUS_CODE: ClassVar[int]

    def __init__(
        self,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message)

        if code is None:
            code = self.DEFAULT_CODE

        if status_code is None:
            status_code = self.DEFAULT_STATUS_CODE

        self._message = message
        self._code = code
        self._status_code = status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def code(self) -> ErrorCode:
        return self._code

    @property
    def status_code(self) -> int:
        return self._status_code

    def into_data(self) -> ErrorData:
        return ErrorData(code=self.code.value, message=self.message)

    @classmethod
    def from_http_error(cls, error: HTTPError) -> Self:
        message = case_fold(error.detail)

        status_code = error.status_code

        code = ErrorCode.from_status_code(status_code)

        return cls(message, code, status_code)

    @classmethod
    def from_validation_error(cls, error: RequestValidationError) -> Self:
        message = VALIDATION_ERROR

        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        code = ErrorCode.from_status_code(status_code)

        return cls(message, code, status_code)


ErrorType = Type[Error]
