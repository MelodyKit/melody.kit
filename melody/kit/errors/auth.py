from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code
from melody.shared.tokens import Scopes

__all__ = (
    # core
    "AuthError",
    # access tokens
    "AuthAccessTokenError",
    "AuthAccessTokenExpected",
    "AuthAccessTokenInvalid",
    "AuthAccessTokenExpectedType",
    "AuthAccessTokenExpectedUser",
    "AuthAccessTokenExpectedUserBased",
    "AuthAccessTokenScopesMissing",
    # refresh tokens
    "AuthRefreshTokenError",
    "AuthRefreshTokenExpected",
    "AuthRefreshTokenInvalid",
    # client credentials
    "AuthClientCredentialsError",
    "AuthClientCredentialsExpected",
    "AuthClientCredentialsInvalid",
    "AuthClientCredentialsMismatch",
    "AuthClientCredentialsNotFound",
    "AuthClientCredentialsSecretMismatch",
    # authorization codes
    "AuthAuthorizationCodeError",
    "AuthAuthorizationCodeExpected",
    "AuthAuthorizationCodeInvalid",
    "AuthAuthorizationCodeRedirectURIExpected",
    "AuthAuthorizationCodeRedirectURIMismatch",
    # verification
    "AuthVerificationCodeError",
    "AuthVerificationCodeInvalid",
    # emails
    "AuthEmailError",
    "AuthEmailInvalid",
    "AuthEmailConflict",
    "AuthEmailFailed",
    "AuthEmailNotFound",
    # passwords
    "AuthPasswordError",
    "AuthPasswordInvalid",
    "AuthPasswordMismatch",
    # codes
    "AuthCodeError",
    "AuthCodeExpected",
    "AuthCodeMismatch",
    "AuthCodeConflict",
    "AuthCodeNotFound",
    # users
    "AuthUserError",
    "AuthUserNotFound",
    "AuthUserUnverified",
)


@default_code(ErrorCode.AUTH_ERROR)
@default_status_code(status.HTTP_401_UNAUTHORIZED)
class AuthError(Error):
    pass


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_ERROR)
class AuthAccessTokenError(AuthError):
    pass


EXPECTED_ACCESS_TOKEN = "expected access token"


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_EXPECTED)
class AuthAccessTokenExpected(AuthAccessTokenError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_ACCESS_TOKEN)


INVALID_ACCESS_TOKEN = "invalid access token"


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_INVALID)
class AuthAccessTokenInvalid(AuthAccessTokenError):
    def __init__(self) -> None:
        super().__init__(INVALID_ACCESS_TOKEN)


ACCESS_TOKENS_EXPECTED_TYPE = "expected `{}` type for access tokens"
access_tokens_expected_type = ACCESS_TOKENS_EXPECTED_TYPE.format


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_EXPECTED_TYPE)
class AuthAccessTokenExpectedType(AuthAccessTokenError):
    def __init__(self, type: str) -> None:
        super().__init__(access_tokens_expected_type(type))


EXPECTED_USER_TOKEN = "expected user token"


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_EXPECTED_USER)
class AuthAccessTokenExpectedUser(AuthAccessTokenError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_USER_TOKEN)


EXPECTED_USER_BASED_TOKEN = "expected user-based token"


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_EXPECTED_USER_BASED)
class AuthAccessTokenExpectedUserBased(AuthAccessTokenError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_USER_BASED_TOKEN)


MISSING_SCOPES = "scopes `{}` missing"
missing_scopes = MISSING_SCOPES.format


@default_code(ErrorCode.AUTH_ACCESS_TOKEN_SCOPES_MISSING)
class AuthAccessTokenScopesMissing(AuthAccessTokenError):
    def __init__(self, scopes: Scopes) -> None:
        super().__init__(missing_scopes(scopes.scope))

        self._scopes = scopes

    @property
    def scopes(self) -> Scopes:
        return self._scopes


@default_code(ErrorCode.AUTH_REFRESH_TOKEN_ERROR)
class AuthRefreshTokenError(AuthError):
    pass


EXPECTED_REFRESH_TOKEN = "expected refresh token"


@default_code(ErrorCode.AUTH_REFRESH_TOKEN_EXPECTED)
class AuthRefreshTokenExpected(AuthRefreshTokenError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_REFRESH_TOKEN)


INVALID_REFRESH_TOKEN = "invalid refresh token"


@default_code(ErrorCode.AUTH_REFRESH_TOKEN_INVALID)
class AuthRefreshTokenInvalid(AuthRefreshTokenError):
    def __init__(self) -> None:
        super().__init__(INVALID_REFRESH_TOKEN)


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_ERROR)
class AuthClientCredentialsError(AuthError):
    pass


EXPECTED_CLIENT_CREDENTIALS = "expected client credentials"


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_EXPECTED)
class AuthClientCredentialsExpected(AuthClientCredentialsError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_CLIENT_CREDENTIALS)


INVALID_CLIENT_CREDENTIALS = "invalid client credentials"


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_INVALID)
class AuthClientCredentialsInvalid(AuthClientCredentialsError):
    def __init__(self) -> None:
        super().__init__(INVALID_CLIENT_CREDENTIALS)


CLIENT_CREDENTIALS_MISMATCH = "client credentials mismatch"


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_MISMATCH)
class AuthClientCredentialsMismatch(AuthClientCredentialsError):
    def __init__(self) -> None:
        super().__init__(CLIENT_CREDENTIALS_MISMATCH)


CLIENT_CREDENTIALS_NOT_FOUND = "client credentials not found"


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_NOT_FOUND)
class AuthClientCredentialsNotFound(AuthClientCredentialsError):
    def __init__(self) -> None:
        super().__init__(CLIENT_CREDENTIALS_NOT_FOUND)


CLIENT_CREDENTIALS_SECRET_MISMATCH = "client credentials secret mismatch"


@default_code(ErrorCode.AUTH_CLIENT_CREDENTIALS_SECRET_MISMATCH)
class AuthClientCredentialsSecretMismatch(AuthClientCredentialsError):
    def __init__(self) -> None:
        super().__init__(CLIENT_CREDENTIALS_SECRET_MISMATCH)


@default_code(ErrorCode.AUTH_AUTHORIZATION_CODE_ERROR)
class AuthAuthorizationCodeError(AuthError):
    pass


EXPECTED_AUTHORIZATION_CODE = "expected authorization code"


@default_code(ErrorCode.AUTH_AUTHORIZATION_CODE_EXPECTED)
class AuthAuthorizationCodeExpected(AuthAuthorizationCodeError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_AUTHORIZATION_CODE)


INVALID_AUTHORIZATION_CODE = "invalid authorization code"


@default_code(ErrorCode.AUTH_AUTHORIZATION_CODE_INVALID)
class AuthAuthorizationCodeInvalid(AuthAuthorizationCodeError):
    def __init__(self) -> None:
        super().__init__(INVALID_AUTHORIZATION_CODE)


REDIRECT_URI_EXPECTED = "redirect URI expected"


@default_code(ErrorCode.AUTH_AUTHORIZATION_CODE_REDIRECT_URI_EXPECTED)
class AuthAuthorizationCodeRedirectURIExpected(AuthAuthorizationCodeError):
    def __init__(self) -> None:
        super().__init__(REDIRECT_URI_EXPECTED)


REDIRECT_URI_MISMATCH = "redirect URI mismatch"


@default_code(ErrorCode.AUTH_AUTHORIZATION_CODE_REDIRECT_URI_MISMATCH)
class AuthAuthorizationCodeRedirectURIMismatch(AuthAuthorizationCodeError):
    def __init__(self) -> None:
        super().__init__(REDIRECT_URI_MISMATCH)


@default_code(ErrorCode.AUTH_VERIFICATION_CODE_ERROR)
class AuthVerificationCodeError(AuthError):
    pass


INVALID_VERIFICATION_CODE = "invalid verification code"


@default_code(ErrorCode.AUTH_VERIFICATION_CODE_INVALID)
class AuthVerificationCodeInvalid(AuthVerificationCodeError):
    def __init__(self) -> None:
        super().__init__(INVALID_VERIFICATION_CODE)


@default_code(ErrorCode.AUTH_EMAIL_ERROR)
class AuthEmailError(AuthError):
    def __init__(
        self,
        email: str,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._email = email

    @property
    def email(self) -> str:
        return self._email


EMAIL_INVALID = "email `{}` is invalid"
email_invalid = EMAIL_INVALID.format


@default_code(ErrorCode.AUTH_EMAIL_INVALID)
class AuthEmailInvalid(AuthEmailError):
    def __init__(self, email: str) -> None:
        super().__init__(email, email_invalid(email))


EMAIL_CONFLICT = "email `{}` conflict"
email_conflict = EMAIL_CONFLICT.format


@default_code(ErrorCode.AUTH_EMAIL_CONFLICT)
class AuthEmailConflict(AuthEmailError):
    def __init__(self, email: str) -> None:
        super().__init__(email, email_conflict(email))


EMAIL_FAILED = "email `{}` failed"
email_failed = EMAIL_FAILED.format


@default_code(ErrorCode.AUTH_EMAIL_FAILED)
class AuthEmailFailed(AuthEmailError):
    def __init__(self, email: str) -> None:
        super().__init__(email, email_failed(email))


EMAIL_NOT_FOUND = "email `{}` not found"
email_not_found = EMAIL_NOT_FOUND.format


@default_code(ErrorCode.AUTH_EMAIL_NOT_FOUND)
class AuthEmailNotFound(AuthEmailError):
    def __init__(self, email: str) -> None:
        super().__init__(email, email_not_found(email))


@default_code(ErrorCode.AUTH_PASSWORD_ERROR)
class AuthPasswordError(AuthError):
    pass


INVALID_PASSWORD = "invalid password"


@default_code(ErrorCode.AUTH_PASSWORD_INVALID)
class AuthPasswordInvalid(AuthPasswordError):
    def __init__(self) -> None:
        super().__init__(INVALID_PASSWORD)


PASSWORD_MISMATCH = "password mismatch"


@default_code(ErrorCode.AUTH_PASSWORD_MISMATCH)
class AuthPasswordMismatch(AuthPasswordError):
    def __init__(self) -> None:
        super().__init__(PASSWORD_MISMATCH)


@default_code(ErrorCode.AUTH_CODE_ERROR)
class AuthCodeError(AuthError):
    pass


EXPECTED_CODE = "expected code"


@default_code(ErrorCode.AUTH_CODE_EXPECTED)
class AuthCodeExpected(AuthCodeError):
    def __init__(self) -> None:
        super().__init__(EXPECTED_CODE)


CODE_MISMATCH = "code mismatch"


@default_code(ErrorCode.AUTH_CODE_MISMATCH)
class AuthCodeMismatch(AuthCodeError):
    def __init__(self) -> None:
        super().__init__(CODE_MISMATCH)


CODE_CONFLICT = "code conflict"


@default_code(ErrorCode.AUTH_CODE_CONFLICT)
class AuthCodeConflict(AuthCodeError):
    def __init__(self) -> None:
        super().__init__(CODE_CONFLICT)


CODE_NOT_FOUND = "code not found"


@default_code(ErrorCode.AUTH_CODE_NOT_FOUND)
class AuthCodeNotFound(AuthCodeError):
    def __init__(self) -> None:
        super().__init__(CODE_NOT_FOUND)


@default_code(ErrorCode.AUTH_USER_ERROR)
class AuthUserError(AuthError):
    def __init__(
        self,
        user_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._user_id = user_id

    @property
    def user_id(self) -> UUID:
        return self._user_id


USER_NOT_FOUND = "user `{}` not found"
user_not_found = USER_NOT_FOUND.format


@default_code(ErrorCode.AUTH_USER_NOT_FOUND)
class AuthUserNotFound(AuthUserError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(user_id, user_not_found(user_id))


USER_UNVERIFIED = "user `{}` is not verified"
user_unverified = USER_UNVERIFIED.format


@default_code(ErrorCode.AUTH_USER_UNVERIFIED)
class AuthUserUnverified(AuthUserError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(user_id, user_unverified(user_id))
