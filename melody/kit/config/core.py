from typing import final

from attrs import Factory, frozen
from pendulum import Duration, duration
from toml import loads as load_string
from typing_aliases import IntoPath
from typing_extensions import Self

from melody.kit.config.defaults import (
    DEFAULT_ACCESS_SIZE,
    DEFAULT_AUTHORIZATION_SIZE,
    DEFAULT_CODE_BORDER,
    DEFAULT_CODE_BOX_SIZE,
    DEFAULT_CODE_CACHE,
    DEFAULT_DOMAIN,
    DEFAULT_EMAIL_HOST,
    DEFAULT_EMAIL_PORT,
    DEFAULT_EMAIL_SUPPORT,
    DEFAULT_EMAIL_TEMPORARY_CONTENT,
    DEFAULT_EMAIL_TEMPORARY_SUBJECT,
    DEFAULT_EMAIL_VERIFICATION_CONTENT,
    DEFAULT_EMAIL_VERIFICATION_SUBJECT,
    DEFAULT_EXPIRES_DAYS,
    DEFAULT_EXPIRES_HOURS,
    DEFAULT_EXPIRES_MINUTES,
    DEFAULT_EXPIRES_MONTHS,
    DEFAULT_EXPIRES_SECONDS,
    DEFAULT_EXPIRES_WEEKS,
    DEFAULT_EXPIRES_YEARS,
    DEFAULT_HASH_MEMORY_COST,
    DEFAULT_HASH_PARALLELISM,
    DEFAULT_HASH_TIME_COST,
    DEFAULT_IMAGE_DATA_LIMIT,
    DEFAULT_IMAGE_DIRECTORY,
    DEFAULT_IMAGE_SIZE_LIMIT,
    DEFAULT_KEYRING_BOT,
    DEFAULT_KEYRING_DISCORD,
    DEFAULT_KEYRING_EMAIL,
    DEFAULT_KEYRING_NAME,
    DEFAULT_KEYRING_SESSION,
    DEFAULT_KEYRING_SPOTIFY,
    DEFAULT_KIT_HOST,
    DEFAULT_KIT_PORT,
    DEFAULT_LIMIT_DEFAULT,
    DEFAULT_LIMIT_MAX,
    DEFAULT_LIMIT_MIN,
    DEFAULT_NAME,
    DEFAULT_OFFSET_DEFAULT,
    DEFAULT_OFFSET_MIN,
    DEFAULT_OPEN,
    DEFAULT_PATH,
    DEFAULT_REDIS_HOST,
    DEFAULT_REDIS_PORT,
    DEFAULT_REFRESH_SIZE,
    DEFAULT_SECRET_SIZE,
    DEFAULT_TOKEN_TYPE,
    DEFAULT_TOTP_DIGITS,
    DEFAULT_TOTP_INTERVAL,
    DEFAULT_TOTP_VALID_WINDOW,
    DEFAULT_VERIFICATION_SIZE,
    DEFAULT_WEB_HOST,
    DEFAULT_WEB_PORT,
)
from melody.kit.enums import ErrorCorrection, LogLevel
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, ROOT
from melody.shared.converter import CONVERTER
from melody.shared.paths import Path, expand_user, prepare_directory
from melody.shared.typing import Data

PATH = expand_user(Path(DEFAULT_PATH))

DEFAULT = ROOT / PATH.name


def prepare_default(path: Path, default: Path) -> None:
    if not path.exists():
        prepare_directory(path.parent)

        path.write_bytes(default.read_bytes())


prepare_default(PATH, DEFAULT)


@final
class KeyringData(Data, total=False):
    name: str
    session: str
    email: str
    bot: str
    discord: str
    spotify: str


@final
@frozen()
class KeyringConfig:
    name: str = DEFAULT_KEYRING_NAME
    session: str = DEFAULT_KEYRING_SESSION
    email: str = DEFAULT_KEYRING_EMAIL
    bot: str = DEFAULT_KEYRING_BOT
    discord: str = DEFAULT_KEYRING_DISCORD
    spotify: str = DEFAULT_KEYRING_SPOTIFY

    @classmethod
    def from_data(cls, data: KeyringData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> KeyringData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class EmailVerificationData(Data, total=False):
    subject: str
    content: str


@final
@frozen()
class EmailVerificationConfig:
    subject: str = DEFAULT_EMAIL_VERIFICATION_SUBJECT
    content: str = DEFAULT_EMAIL_VERIFICATION_CONTENT

    @classmethod
    def from_data(cls, data: EmailVerificationData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EmailVerificationData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class EmailTemporaryData(Data, total=False):
    subject: str
    content: str


@final
@frozen()
class EmailTemporaryConfig:
    subject: str = DEFAULT_EMAIL_TEMPORARY_SUBJECT
    content: str = DEFAULT_EMAIL_TEMPORARY_CONTENT

    @classmethod
    def from_data(cls, data: EmailTemporaryData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EmailTemporaryData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class EmailData(Data, total=False):
    host: str
    port: int
    support: str

    verification: EmailVerificationData
    temporary: EmailTemporaryData


@final
@frozen()
class EmailConfig:
    host: str = DEFAULT_EMAIL_HOST
    port: int = DEFAULT_EMAIL_PORT
    support: str = DEFAULT_EMAIL_SUPPORT

    verification: EmailVerificationConfig = Factory(EmailVerificationConfig)
    temporary: EmailTemporaryConfig = Factory(EmailTemporaryConfig)

    @classmethod
    def from_data(cls, data: EmailData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EmailData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class HashData(Data, total=False):
    time_cost: int
    memory_cost: int
    parallelism: int


@final
@frozen()
class HashConfig:
    time_cost: int = DEFAULT_HASH_TIME_COST
    memory_cost: int = DEFAULT_HASH_MEMORY_COST
    parallelism: int = DEFAULT_HASH_PARALLELISM

    @classmethod
    def from_data(cls, data: HashData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> HashData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class KitData(Data, total=False):
    host: str
    port: int


@final
@frozen()
class KitConfig:
    host: str = DEFAULT_KIT_HOST
    port: int = DEFAULT_KIT_PORT

    @classmethod
    def from_data(cls, data: KitData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> KitData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class CodeData(Data, total=False):
    cache: str
    error_correction: str
    box_size: int
    border: int


@final
@frozen()
class CodeConfig:
    cache: str = DEFAULT_CODE_CACHE
    error_correction: ErrorCorrection = ErrorCorrection.DEFAULT
    box_size: int = DEFAULT_CODE_BOX_SIZE
    border: int = DEFAULT_CODE_BORDER

    def __attrs_post_init__(self) -> None:
        prepare_directory(self.cache_path)

    @property
    def cache_path(self) -> Path:
        return expand_user(Path(self.cache))

    # TODO: cache `Path`

    @classmethod
    def from_data(cls, data: CodeData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> CodeData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class ImageData(Data, total=False):
    directory: str
    size_limit: int
    data_limit: int


@final
@frozen()
class ImageConfig:
    directory: str = DEFAULT_IMAGE_DIRECTORY
    size_limit: int = DEFAULT_IMAGE_SIZE_LIMIT
    data_limit: int = DEFAULT_IMAGE_DATA_LIMIT

    def __attrs_post_init__(self) -> None:
        prepare_directory(self.directory_path)

    @property
    def directory_path(self) -> Path:
        return expand_user(Path(self.directory))

    # TODO: directory `Path`

    @classmethod
    def from_data(cls, data: ImageData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ImageData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class LogData(Data, total=False):
    level: str


@final
@frozen()
class LogConfig:
    level: LogLevel = LogLevel.DEFAULT

    @classmethod
    def from_data(cls, data: LogData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> LogData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class RedisData(Data, total=False):
    host: str
    port: int


@final
@frozen()
class RedisConfig:
    host: str = DEFAULT_REDIS_HOST
    port: int = DEFAULT_REDIS_PORT

    @classmethod
    def from_data(cls, data: RedisData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> RedisData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class SecretData(Data, total=False):
    size: int


@final
@frozen()
class SecretConfig:
    size: int = DEFAULT_SECRET_SIZE

    @classmethod
    def from_data(cls, data: SecretData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SecretData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class TOTPData(Data, total=False):
    digits: int
    interval: int
    valid_window: int


@final
@frozen()
class TOTPConfig:
    digits: int = DEFAULT_TOTP_DIGITS
    interval: int = DEFAULT_TOTP_INTERVAL
    valid_window: int = DEFAULT_TOTP_VALID_WINDOW

    @classmethod
    def from_data(cls, data: TOTPData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TOTPData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class ExpiresData(Data, total=False):
    years: int
    months: int
    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int


@final
@frozen()
class ExpiresConfig:
    years: int = DEFAULT_EXPIRES_YEARS
    months: int = DEFAULT_EXPIRES_MONTHS
    weeks: int = DEFAULT_EXPIRES_WEEKS
    days: int = DEFAULT_EXPIRES_DAYS
    hours: int = DEFAULT_EXPIRES_HOURS
    minutes: int = DEFAULT_EXPIRES_MINUTES
    seconds: int = DEFAULT_EXPIRES_SECONDS

    @property
    def duration(self) -> Duration:
        return duration(
            years=self.years,
            months=self.months,
            weeks=self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
        )

    @classmethod
    def from_data(cls, data: ExpiresData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExpiresData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class AccessData(Data, total=False):
    size: int
    expires: ExpiresData


@final
@frozen()
class AccessConfig:
    size: int = DEFAULT_ACCESS_SIZE
    expires: ExpiresConfig = Factory(ExpiresConfig)

    @classmethod
    def from_data(cls, data: AccessData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AccessData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class RefreshData(Data, total=False):
    size: int
    expires: ExpiresData


@final
@frozen()
class RefreshConfig:
    size: int = DEFAULT_REFRESH_SIZE
    expires: ExpiresConfig = Factory(ExpiresConfig)

    @classmethod
    def from_data(cls, data: RefreshData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> RefreshData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class AuthorizationData(Data, total=False):
    size: int
    expires: ExpiresData


@final
@frozen()
class AuthorizationConfig:
    size: int = DEFAULT_AUTHORIZATION_SIZE
    expires: ExpiresConfig = Factory(ExpiresConfig)

    @classmethod
    def from_data(cls, data: AuthorizationData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AuthorizationData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class VerificationData(Data, total=False):
    size: int
    expires: ExpiresData


@final
@frozen()
class VerificationConfig:
    size: int = DEFAULT_VERIFICATION_SIZE
    expires: ExpiresConfig = Factory(ExpiresConfig)

    @classmethod
    def from_data(cls, data: VerificationData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> VerificationData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class TokenData(Data, total=False):
    type: str


@final
@frozen()
class TokenConfig:
    type: str = DEFAULT_TOKEN_TYPE

    @classmethod
    def from_data(cls, data: TokenData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TokenData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class WebData(Data, total=False):
    host: str
    port: int


@final
@frozen()
class WebConfig:
    host: str = DEFAULT_WEB_HOST
    port: int = DEFAULT_WEB_PORT

    @classmethod
    def from_data(cls, data: WebData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> WebData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class OffsetData(Data, total=False):
    default: int
    min: int


@final
@frozen()
class OffsetConfig:
    default: int = DEFAULT_OFFSET_DEFAULT
    min: int = DEFAULT_OFFSET_MIN

    @classmethod
    def from_data(cls, data: OffsetData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> OffsetData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class LimitData(Data, total=False):
    default: int
    min: int
    max: int


@final
@frozen()
class LimitConfig:
    default: int = DEFAULT_LIMIT_DEFAULT
    min: int = DEFAULT_LIMIT_MIN
    max: int = DEFAULT_LIMIT_MAX

    @classmethod
    def from_data(cls, data: LimitData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> LimitData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


@final
class ConfigData(Data, total=False):
    name: str
    domain: str
    open: str

    keyring: KeyringData
    email: EmailData
    hash: HashData
    kit: KitData
    code: CodeData
    image: ImageData
    log: LogData
    redis: RedisData
    secret: SecretData
    totp: TOTPData
    token: TokenData
    access: AccessData
    refresh: RefreshData
    authorization: AuthorizationData
    verification: VerificationData
    web: WebData
    offset: OffsetData
    limit: LimitData


@final
@frozen()
class Config:
    name: str = DEFAULT_NAME
    domain: str = DEFAULT_DOMAIN
    open: str = DEFAULT_OPEN

    keyring: KeyringConfig = Factory(KeyringConfig)
    email: EmailConfig = Factory(EmailConfig)
    hash: HashConfig = Factory(HashConfig)
    kit: KitConfig = Factory(KitConfig)
    code: CodeConfig = Factory(CodeConfig)
    image: ImageConfig = Factory(ImageConfig)
    log: LogConfig = Factory(LogConfig)
    redis: RedisConfig = Factory(RedisConfig)
    secret: SecretConfig = Factory(SecretConfig)
    totp: TOTPConfig = Factory(TOTPConfig)
    token: TokenConfig = Factory(TokenConfig)
    access: AccessConfig = Factory(AccessConfig)
    refresh: RefreshConfig = Factory(RefreshConfig)
    authorization: AuthorizationConfig = Factory(AuthorizationConfig)
    verification: VerificationConfig = Factory(VerificationConfig)
    web: WebConfig = Factory(WebConfig)
    offset: OffsetConfig = Factory(OffsetConfig)
    limit: LimitConfig = Factory(LimitConfig)

    @classmethod
    def from_data(cls, data: ConfigData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ConfigData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    @classmethod
    def from_string(cls, string: str) -> Self:
        return cls.from_data(load_string(string))  # type: ignore[arg-type]

    @classmethod
    def from_path(
        cls, path: IntoPath, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
    ) -> Self:
        return cls.from_string(Path(path).read_text(encoding, errors))


CONFIG = Config.from_path(PATH)
