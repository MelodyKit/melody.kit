from melody.kit import endpoints, models
from melody.kit.config import Config, ConfigData, get_config, get_default_config
from melody.kit.core import app, config, database, hasher, redis, v1
from melody.kit.database import Database
from melody.kit.enums import AlbumType, EntityType, LogLevel, PrivacyType
from melody.kit.errors import (
    AnyError,
    AuthenticationError,
    AuthenticationInvalid,
    AuthenticationMissing,
    AuthenticationNotFound,
    BadRequest,
    Conflict,
    Error,
    ErrorCode,
    ErrorData,
    Forbidden,
    Gone,
    InternalError,
    MethodNotAllowed,
    NotFound,
    PayloadTooLarge,
    RateLimited,
    Unauthorized,
    ValidationError,
)
from melody.kit.tokens import (
    Token,
    TokenData,
    delete_token,
    delete_tokens_for,
    fetch_tokens_for,
    fetch_user_id_by,
    generate_token_for,
    token_factory,
    token_from_data,
    token_into_data,
)
from melody.kit.uri import URI

__all__ = (
    # endpoints
    "endpoints",
    # models
    "models",
    # core
    "config",
    "database",
    "redis",
    "hasher",
    "app",
    "v1",
    # config
    "Config",
    "ConfigData",
    "get_config",
    "get_default_config",
    # database
    "Database",
    # enums
    "AlbumType",
    "PrivacyType",
    "EntityType",
    "LogLevel",
    # errors
    "AnyError",
    "Error",
    "ErrorCode",
    "ErrorData",
    "AuthenticationError",
    "AuthenticationInvalid",
    "AuthenticationMissing",
    "AuthenticationNotFound",
    "ValidationError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "MethodNotAllowed",
    "Conflict",
    "Gone",
    "PayloadTooLarge",
    "RateLimited",
    "InternalError",
    # tokens
    "Token",
    "TokenData",
    "token_factory",
    "token_from_data",
    "token_into_data",
    "generate_token_for",
    "delete_token",
    "delete_tokens_for",
    "fetch_user_id_by",
    "fetch_tokens_for",
    # URI
    "URI",
)
