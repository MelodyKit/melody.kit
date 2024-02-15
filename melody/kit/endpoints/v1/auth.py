from typing import Optional
from typing_extensions import Annotated

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import Form
from typing_aliases import NormalError

from melody.kit.authorization import (
    OptionalAuthorizationCodeDependency, delete_authorization_codes_with
)
from melody.kit.contexts import ClientContext, Context, UserContext
from melody.kit.core import database, hasher, v1
from melody.kit.dependencies import EmailDeliverabilityDependency, EmailDependency
from melody.kit.email import email_message, send_email_message, support
from melody.kit.endpoints.v1.totp import validate_totp
from melody.kit.enums import Tag
from melody.kit.errors import AuthInvalid, Conflict, NotFound, Unauthorized
from melody.kit.models.base import BaseData
from melody.kit.oauth2 import (
    BoundTokenDependency,
    OptionalBoundRefreshTokenDependency,
    OptionalClientCredentialsDependency,
    TokenDependency,
    UserTokenDependency,
)
from melody.kit.tokens import (
    delete_access_token,
    delete_access_tokens_with,
    delete_refresh_token,
    delete_refresh_tokens_with,
    generate_tokens_with,
)
from melody.kit.verification import (
    VerificationCodeDependency,
    delete_verification_code,
    delete_verification_codes_for,
    generate_verification_code_for,
)
from melody.shared.enums import GrantType
from melody.shared.markers import unreachable
from melody.shared.tokens import TokensData

__all__ = (
    "login",
    "revoke",
    "tokens",
    "revoke_all",
    "register",
    "verify",
    "reset",
    "forgot",
)

CAN_NOT_FIND_USER_BY_EMAIL = "can not find the user with the email `{}`"
can_not_find_user_by_email = CAN_NOT_FIND_USER_BY_EMAIL.format

PASSWORD_MISMATCH = "password mismatch"

UNVERIFIED = "user with ID `{}` is not verified"
unverified = UNVERIFIED.format

CAN_NOT_FIND_USER = "can not find the user with the ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format


PasswordDependency = Annotated[str, Form()]
CodeDependency = Annotated[Optional[str], Form()]


@v1.post(
    "/login",
    tags=[Tag.AUTH],
    summary="Logs in the user.",
)
async def login(
    email: EmailDependency,
    password: PasswordDependency,
    code: CodeDependency = None,
) -> TokensData:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise NotFound(can_not_find_user_by_email(email))

    user_id = user_info.id

    if not user_info.is_verified():
        raise Unauthorized(unverified(user_id))

    password_hash = user_info.password_hash

    try:
        hasher.verify(password_hash, password)

    except VerifyMismatchError:
        raise Unauthorized(PASSWORD_MISMATCH) from None

    secret = user_info.secret

    validate_totp(secret, code)

    context = UserContext(user_id)

    tokens = await generate_tokens_with(context)

    if hasher.check_needs_rehash(password_hash):
        password_hash = hasher.hash(password)

        await database.update_user_password_hash(user_id=user_id, password_hash=password_hash)

    return tokens.into_data()


@v1.post(
    "/revoke",
    tags=[Tag.AUTH],
    summary="Revokes the token.",
)
async def revoke(bound_token: BoundTokenDependency) -> None:
    await delete_access_token(bound_token.token)


EXPECTED_CODE = "expected code for `authorization_code` grant type"
INVALID_CODE = "invalid code"

EXPECTED_CLIENT_CREDENTIALS = "expected client credentials"
CLIENT_CREDENTIALS_MISMATCH = "client credentials mismatch"

EXPECTED_REFRESH_TOKEN = "expected refresh token for `refresh_token` grant type"
INVALID_REFRESH_TOKEN = "invalid refresh token"


GrantTypeDependency = Annotated[GrantType, Form()]


@v1.post("/tokens", tags=[Tag.AUTH], summary="Returns tokens.")
async def tokens(
    grant_type: GrantTypeDependency,
    authorization_context: OptionalAuthorizationCodeDependency = None,
    bound_refresh_token: OptionalBoundRefreshTokenDependency = None,
    client_credentials: OptionalClientCredentialsDependency = None,
) -> TokensData:
    context: Optional[Context] = None

    if grant_type.is_authorization_code():
        if authorization_context is None:
            raise AuthInvalid(EXPECTED_CODE)

        if client_credentials is None:
            raise AuthInvalid(EXPECTED_CLIENT_CREDENTIALS)

        if client_credentials.id != authorization_context.client_id:
            raise AuthInvalid(CLIENT_CREDENTIALS_MISMATCH)

        await delete_authorization_codes_with(authorization_context)

        context = authorization_context.into_context()

    if grant_type.is_client_credentials():
        if client_credentials is None:
            raise AuthInvalid(EXPECTED_CLIENT_CREDENTIALS)

        client_id = client_credentials.id

        context = ClientContext(client_id)

    if grant_type.is_refresh_token():
        if bound_refresh_token is None:
            raise AuthInvalid(EXPECTED_REFRESH_TOKEN)

        await delete_refresh_token(bound_refresh_token.token)

        context = bound_refresh_token.context

    if context is None:
        unreachable()

    tokens = await generate_tokens_with(context)

    return tokens.into_data()


@v1.post(
    "/revoke-all",
    tags=[Tag.AUTH],
    summary="Revokes all tokens.",
)
async def revoke_all(context: TokenDependency) -> None:
    await delete_access_tokens_with(context)
    await delete_refresh_tokens_with(context)


EMAIL_TAKEN = "the email `{}` is taken"
email_taken = EMAIL_TAKEN.format

VERIFICATION = "MelodyKit verification code"
VERIFICATION_CONTENT = """
Here is your verification code:

{verification_code}
""".strip()
verification_content = VERIFICATION_CONTENT.format


NameDependency = Annotated[str, Form()]


@v1.post(
    "/register",
    tags=[Tag.AUTH],
    summary="Registers the user.",
)
async def register(
    name: NameDependency,
    email: EmailDeliverabilityDependency,
    password: PasswordDependency,
) -> BaseData:
    password_hash = hasher.hash(password)

    try:
        self = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise Conflict(email_taken(email)) from None

    else:
        self_id = self.id

        verification_code = await generate_verification_code_for(self_id)

        try:
            await send_email_message(
                email_message(
                    author=support(),
                    target=email,
                    subject=VERIFICATION,
                    content=verification_content(verification_code=verification_code),
                )
            )

        except NormalError:
            await database.delete_user(user_id=self_id)
            await delete_verification_code(verification_code)

            raise

        return self.into_data()


@v1.post(
    "/verify",
    tags=[Tag.AUTH],
    summary="Verifies the user.",
)
async def verify(self_id: VerificationCodeDependency) -> None:
    await delete_verification_codes_for(self_id)

    await database.update_user_verified(user_id=self_id, verified=True)


@v1.post(
    "/reset",
    tags=[Tag.AUTH],
    summary="Resets the password of the user, revoking all their tokens.",
)
async def reset(context: UserTokenDependency, password: PasswordDependency) -> None:
    await revoke_all(context)

    self_id = context.user_id

    password_hash = hasher.hash(password)

    await database.update_user_password_hash(user_id=self_id, password_hash=password_hash)


TEMPORARY_TOKEN = "MelodyKit temporary token"
TEMPORARY_TOKEN_CONTENT = """
Here is your temporary token:

{temporary_token}
""".strip()
temporary_token_content = TEMPORARY_TOKEN_CONTENT.format


@v1.post(
    "/forgot",
    tags=[Tag.AUTH],
    summary="Allows the user to reset their password via the email.",
)
async def forgot(email: EmailDependency, code: CodeDependency = None) -> None:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise NotFound(can_not_find_user_by_email(email))

    secret = user_info.secret

    validate_totp(secret, code)

    context = UserContext(user_info.id)

    tokens = await generate_tokens_with(context)

    temporary_token = tokens.access_token

    await send_email_message(
        email_message(
            author=support(),
            target=email,
            subject=TEMPORARY_TOKEN,
            content=temporary_token_content(temporary_token=temporary_token),
        )
    )
