from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from edgedb import ConstraintViolationError
from fastapi import BackgroundTasks, Form
from typing_aliases import NormalError
from typing_extensions import Annotated

from melody.kit.authorization.code import AuthorizationCode, AuthorizationCodeData
from melody.kit.authorization.context import AuthorizationContext
from melody.kit.authorization.dependencies import OptionalAuthorizationCodeDependency
from melody.kit.authorization.operations import (
    delete_authorization_codes_with,
    generate_authorization_code_with,
)
from melody.kit.clients.dependencies import OptionalClientCredentialsDependency
from melody.kit.core import config, database, hasher, v1
from melody.kit.dependencies.emails import EmailDeliverabilityDependency, EmailDependency
from melody.kit.dependencies.scopes import ScopesDependency
from melody.kit.emails import email_message, send_email_message, support
from melody.kit.enums import Tag
from melody.kit.errors.auth import (
    AuthAuthorizationCodeExpected,
    AuthAuthorizationCodeRedirectURIExpected,
    AuthAuthorizationCodeRedirectURIMismatch,
    AuthClientCredentialsExpected,
    AuthClientCredentialsMismatch,
    AuthEmailConflict,
    AuthEmailFailed,
    AuthEmailNotFound,
    AuthPasswordMismatch,
    AuthRefreshTokenExpected,
    AuthUserUnverified,
)
from melody.kit.models.base import BaseData
from melody.kit.tokens.context import ClientContext, Context, UserContext
from melody.kit.tokens.dependencies import (
    BoundTokenDependency,
    OptionalBoundRefreshTokenDependency,
    TokenDependency,
    UserTokenDependency,
)
from melody.kit.tokens.operations import (
    delete_access_token,
    delete_access_tokens_with,
    delete_refresh_token,
    delete_refresh_tokens_with,
    generate_tokens_with,
)
from melody.kit.totp.core import validate_totp
from melody.kit.totp.dependencies import OptionalCodeDependency
from melody.kit.verification.dependencies import VerificationCodeDependency
from melody.kit.verification.operations import (
    delete_verification_code,
    delete_verification_codes_for,
    generate_verification_code_for,
)
from melody.shared.enums import GrantType
from melody.shared.markers import unreachable
from melody.shared.tokens import TokensData

__all__ = (
    "login",
    "authorize",
    "revoke",
    "tokens",
    "revoke_all",
    "register",
    "verify",
    "reset",
    "forgot",
)


PasswordDependency = Annotated[str, Form()]


@v1.post(
    "/login",
    tags=[Tag.AUTH],
    summary="Logs in the user.",
)
async def login(
    email: EmailDependency,
    password: PasswordDependency,
    code: OptionalCodeDependency = None,
) -> TokensData:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise AuthEmailNotFound(email)

    user_id = user_info.id

    if not user_info.is_verified():
        raise AuthUserUnverified(user_id)

    password_hash = user_info.password_hash

    try:
        hasher.verify(password_hash, password)

    except VerifyMismatchError:
        raise AuthPasswordMismatch() from None

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


ClientIDDependency = Annotated[UUID, Form()]
RedirectURIDependency = Annotated[str, Form()]
StateDependency = Annotated[str, Form()]


@v1.post("/authorize", tags=[Tag.AUTH], summary="Authorizes the client to access the user's data.")
async def authorize(
    context: UserTokenDependency,
    client_id: ClientIDDependency,
    scopes: ScopesDependency,
    redirect_uri: RedirectURIDependency,
    state: StateDependency,
) -> AuthorizationCodeData:
    authorization_context = AuthorizationContext(
        user_id=context.user_id, client_id=client_id, scopes=scopes, redirect_uri=redirect_uri
    )

    code = await generate_authorization_code_with(authorization_context)

    authorization_code = AuthorizationCode(code, state)

    return authorization_code.into_data()


GrantTypeDependency = Annotated[GrantType, Form()]

OptionalRedirectURIDependency = Annotated[Optional[str], Form()]


@v1.post("/tokens", tags=[Tag.AUTH], summary="Returns tokens.")
async def tokens(
    grant_type: GrantTypeDependency,
    redirect_uri: OptionalRedirectURIDependency = None,
    authorization_context: OptionalAuthorizationCodeDependency = None,
    bound_refresh_token: OptionalBoundRefreshTokenDependency = None,
    client_credentials: OptionalClientCredentialsDependency = None,
) -> TokensData:
    context: Optional[Context] = None

    if grant_type.is_authorization_code():
        if authorization_context is None:
            raise AuthAuthorizationCodeExpected()

        if redirect_uri is None:
            raise AuthAuthorizationCodeRedirectURIExpected()

        if client_credentials is None:
            raise AuthClientCredentialsExpected()

        if client_credentials.id != authorization_context.client_id:
            raise AuthClientCredentialsMismatch()

        if redirect_uri != authorization_context.redirect_uri:
            raise AuthAuthorizationCodeRedirectURIMismatch()

        await delete_authorization_codes_with(authorization_context)

        context = authorization_context.into_context()

    if grant_type.is_client_credentials():
        if client_credentials is None:
            raise AuthClientCredentialsExpected()

        client_id = client_credentials.id

        context = ClientContext(client_id)

    if grant_type.is_refresh_token():
        if bound_refresh_token is None:
            raise AuthRefreshTokenExpected()

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
    background_tasks: BackgroundTasks,
) -> BaseData:
    password_hash = hasher.hash(password)

    try:
        self = await database.insert_user(name=name, email=email, password_hash=password_hash)

    except ConstraintViolationError:
        raise AuthEmailConflict(email) from None

    else:
        self_id = self.id

        verification_code = await generate_verification_code_for(self_id)

        verification_config = config.email.verification

        try:
            await send_email_message(
                email_message(
                    author=support(),
                    target=email,
                    subject=verification_config.subject.format(name=config.name),
                    content=verification_config.content.format(verification_code=verification_code),
                )
            )

        except NormalError:
            await database.delete_user(user_id=self_id)
            await delete_verification_code(verification_code)

            raise AuthEmailFailed(email) from None

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


@v1.post(
    "/forgot",
    tags=[Tag.AUTH],
    summary="Allows the user to reset their password via the email.",
)
async def forgot(email: EmailDependency, code: OptionalCodeDependency = None) -> None:
    user_info = await database.query_user_info_by_email(email=email)

    if user_info is None:
        raise AuthEmailNotFound(email)

    secret = user_info.secret

    validate_totp(secret, code)

    context = UserContext(user_info.id)

    tokens = await generate_tokens_with(context)

    await delete_refresh_token(tokens.refresh_token)

    temporary_token = tokens.access_token

    temporary_config = config.email.temporary

    try:
        await send_email_message(
            email_message(
                author=support(),
                target=email,
                subject=temporary_config.subject.format(name=config.name),
                content=temporary_config.content.format(temporary_token=temporary_token),
            )
        )

    except NormalError:
        await delete_access_token(temporary_token)

        raise AuthEmailFailed(email) from None
