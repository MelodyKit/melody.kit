from pathlib import Path
from typing import Any, Type, TypeVar, cast

from attrs import define
from toml import loads as load_string
from wraps.option import Option
from wraps.wraps import wrap_optional

from melody.kit.constants import DEFAULT_IGNORE_SENSITIVE
from melody.kit.enums import ErrorCorrection, LogLevel
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, EMPTY, HOME, ROOT
from melody.shared.typing import IntoPath, StringDict

__all__ = ("Config", "ConfigData", "get_config", "get_default_config")

T = TypeVar("T")


def expand_user_directory(path: Path) -> Path:
    directory = path.expanduser()

    directory.mkdir(parents=True, exist_ok=True)

    return directory


CONFIG_NAME = ".config"
MELODY_NAME = "melody"

NAME = "kit.toml"

DEFAULT_PATH = ROOT / NAME
PATH = HOME / CONFIG_NAME / MELODY_NAME / NAME


if not PATH.exists():
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_bytes(DEFAULT_PATH.read_bytes())


class ConfigData(StringDict[T]):
    def __getattr__(self, name: str) -> Option[T]:
        return wrap_optional(self.get(name))


AnyConfigData = ConfigData[Any]


@define()
class EmailConfig:
    host: str
    port: int
    support: str
    name: str
    password: str


@define()
class HashConfig:
    time_cost: int
    memory_cost: int
    parallelism: int


@define()
class KitConfig:
    host: str
    port: int


@define()
class LinkConfig:
    cache: Path
    error_correction: ErrorCorrection
    box_size: int
    border: int


@define()
class LogConfig:
    level: LogLevel


@define()
class RedisConfig:
    host: str
    port: int


@define()
class ExpiresConfig:
    years: float
    months: float
    weeks: float
    days: float
    hours: float
    minutes: float
    seconds: float


@define()
class TokenConfig:
    size: int
    type: str
    expires: ExpiresConfig


@define()
class WebConfig:
    host: str
    port: int


@define()
class BotConfig:
    token: str


EXPECTED = "expected `{}`"
expected = EXPECTED.format


EXPECTED_MELODY = expected("melody")
EXPECTED_MELODY_NAME = expected("melody.name")
EXPECTED_MELODY_DOMAIN = expected("melody.domain")
EXPECTED_MELODY_OPEN = expected("melody.open")
EXPECTED_MELODY_IMAGES = expected("melody.images")
EXPECTED_MELODY_EMAIL = expected("melody.email")
EXPECTED_MELODY_EMAIL_HOST = expected("melody.email.host")
EXPECTED_MELODY_EMAIL_PORT = expected("melody.email.port")
EXPECTED_MELODY_EMAIL_SUPPORT = expected("melody.email.support")
EXPECTED_MELODY_EMAIL_NAME = expected("melody.email.name")
EXPECTED_MELODY_EMAIL_PASSWORD = expected("melody.email.password")
EXPECTED_MELODY_HASH = expected("melody.hash")
EXPECTED_MELODY_HASH_TIME_COST = expected("melody.hash.time_cost")
EXPECTED_MELODY_HASH_MEMORY_COST = expected("melody.hash.memory_cost")
EXPECTED_MELODY_HASH_PARALLELISM = expected("melody.hash.parallelism")
EXPECTED_MELODY_KIT = expected("melody.kit")
EXPECTED_MELODY_KIT_HOST = expected("melody.kit.host")
EXPECTED_MELODY_KIT_PORT = expected("melody.kit.port")
EXPECTED_MELODY_LINK = expected("melody.link")
EXPECTED_MELODY_LINK_CACHE = expected("melody.link.cache")
EXPECTED_MELODY_LINK_ERROR_CORRECTION = expected("melody.link.error_correction")
EXPECTED_MELODY_LINK_BOX_SIZE = expected("melody.link.box_size")
EXPECTED_MELODY_LINK_BORDER = expected("melody.link.border")
EXPECTED_MELODY_LOG = expected("melody.log")
EXPECTED_MELODY_LOG_LEVEL = expected("melody.log.level")
EXPECTED_MELODY_REDIS = expected("melody.redis")
EXPECTED_MELODY_REDIS_HOST = expected("melody.redis.host")
EXPECTED_MELODY_REDIS_PORT = expected("melody.redis.port")
EXPECTED_MELODY_TOKEN = expected("melody.token")
EXPECTED_MELODY_TOKEN_SIZE = expected("melody.token.size")
EXPECTED_MELODY_TOKEN_TYPE = expected("melody.token.type")
EXPECTED_MELODY_TOKEN_EXPIRES = expected("melody.token.expires")
EXPECTED_MELODY_TOKEN_EXPIRES_YEARS = expected("melody.token.expires.years")
EXPECTED_MELODY_TOKEN_EXPIRES_MONTHS = expected("melody.token.expires.months")
EXPECTED_MELODY_TOKEN_EXPIRES_WEEKS = expected("melody.token.expires.weeks")
EXPECTED_MELODY_TOKEN_EXPIRES_DAYS = expected("melody.token.expires.days")
EXPECTED_MELODY_TOKEN_EXPIRES_HOURS = expected("melody.token.expires.hours")
EXPECTED_MELODY_TOKEN_EXPIRES_MINUTES = expected("melody.token.expires.minutes")
EXPECTED_MELODY_TOKEN_EXPIRES_SECONDS = expected("melody.token.expires.seconds")
EXPECTED_MELODY_WEB = expected("melody.web")
EXPECTED_MELODY_WEB_HOST = expected("melody.web.host")
EXPECTED_MELODY_WEB_PORT = expected("melody.web.port")
EXPECTED_MELODY_BOT = expected("melody.bot")
EXPECTED_MELODY_BOT_TOKEN = expected("melody.bot.token")

C = TypeVar("C", bound="Config")


@define()
class Config:
    name: str
    domain: str
    open: str
    images: Path
    email: EmailConfig
    hash: HashConfig
    kit: KitConfig
    link: LinkConfig
    log: LogConfig
    redis: RedisConfig
    token: TokenConfig
    web: WebConfig
    bot: BotConfig

    def ensure_directories(self: C) -> C:
        self.images = expand_user_directory(self.images)

        link = self.link

        link.cache = expand_user_directory(link.cache)

        return self

    @classmethod
    def from_string(cls: Type[C], string: str) -> C:
        return cls.from_data(cls.parse(string))

    @classmethod
    def from_path(
        cls: Type[C], path: IntoPath, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
    ) -> C:
        return cls.from_string(Path(path).read_text(encoding, errors))

    @staticmethod
    def parse(string: str) -> AnyConfigData:
        return cast(AnyConfigData, load_string(string, AnyConfigData))

    @classmethod
    def from_data(cls: Type[C], data: AnyConfigData) -> C:
        default_config = DEFAULT_CONFIG

        config_data = data.melody.unwrap_or_else(AnyConfigData)

        email_data = config_data.email.unwrap_or_else(AnyConfigData)
        email_config = default_config.email

        email = EmailConfig(
            host=email_data.host.unwrap_or(email_config.host),
            port=email_data.port.unwrap_or(email_config.port),
            support=email_data.support.unwrap_or(email_config.support),
            name=email_data.name.expect(EXPECTED_MELODY_EMAIL_NAME),
            password=email_data.password.expect(EXPECTED_MELODY_EMAIL_PASSWORD),
        )

        hash_data = config_data.hash.unwrap_or_else(AnyConfigData)
        hash_config = default_config.hash

        hash = HashConfig(
            time_cost=hash_data.time_cost.unwrap_or(hash_config.time_cost),
            memory_cost=hash_data.memory_cost.unwrap_or(hash_config.memory_cost),
            parallelism=hash_data.parallelism.unwrap_or(hash_config.parallelism),
        )

        kit_data = config_data.kit.unwrap_or_else(AnyConfigData)
        kit_config = default_config.kit

        kit = KitConfig(
            host=kit_data.host.unwrap_or(kit_config.host),
            port=kit_data.port.unwrap_or(kit_config.port),
        )

        link_data = config_data.link.unwrap_or_else(AnyConfigData)
        link_config = default_config.link

        link = LinkConfig(
            cache=link_data.cache.map_or(link_config.cache, Path),
            error_correction=link_data.error_correction.map_or(
                link_config.error_correction, ErrorCorrection
            ),
            box_size=link_data.box_size.unwrap_or(link_config.box_size),
            border=link_data.border.unwrap_or(link_config.border),
        )

        log_data = config_data.log.unwrap_or_else(AnyConfigData)
        log_config = default_config.log

        log = LogConfig(level=log_data.level.unwrap_or(log_config.level))

        redis_data = config_data.redis.unwrap_or_else(AnyConfigData)
        redis_config = default_config.redis

        redis = RedisConfig(
            host=redis_data.host.unwrap_or(redis_config.host),
            port=redis_data.port.unwrap_or(redis_config.port),
        )

        token_data = config_data.token.unwrap_or_else(AnyConfigData)
        token_config = default_config.token

        expires_data = token_data.expires.unwrap_or_else(AnyConfigData)
        expires_config = token_config.expires

        token = TokenConfig(
            size=token_data.size.unwrap_or(token_config.size),
            type=token_data.type.unwrap_or(token_config.type),
            expires=ExpiresConfig(
                years=expires_data.years.unwrap_or(expires_config.years),
                months=expires_data.months.unwrap_or(expires_config.months),
                weeks=expires_data.weeks.unwrap_or(expires_config.weeks),
                days=expires_data.days.unwrap_or(expires_config.days),
                hours=expires_data.hours.unwrap_or(expires_config.hours),
                minutes=expires_data.minutes.unwrap_or(expires_config.minutes),
                seconds=expires_data.seconds.unwrap_or(expires_config.seconds),
            ),
        )

        bot_data = config_data.bot.unwrap_or_else(AnyConfigData)
        # bot_config = default_config.bot

        bot = BotConfig(token=bot_data.token.expect(EXPECTED_MELODY_BOT_TOKEN))

        web_data = config_data.web.unwrap_or_else(AnyConfigData)
        web_config = default_config.web

        web = WebConfig(
            host=web_data.host.unwrap_or(web_config.host),
            port=web_data.port.unwrap_or(web_config.port),
        )

        name = config_data.name.unwrap_or(default_config.name)
        domain = config_data.domain.unwrap_or(default_config.domain)
        open = config_data.open.unwrap_or(default_config.open)
        images = config_data.images.map_or(default_config.images, Path)

        return cls(
            name=name,
            domain=domain,
            open=open,
            images=images,
            email=email,
            hash=hash,
            kit=kit,
            link=link,
            log=log,
            redis=redis,
            token=token,
            web=web,
            bot=bot,
        )

    @classmethod
    def unsafe_from_string(
        cls: Type[C], string: str, ignore_sensitive: bool = DEFAULT_IGNORE_SENSITIVE
    ) -> C:
        return cls.unsafe_from_data(cls.parse(string), ignore_sensitive=ignore_sensitive)

    @classmethod
    def unsafe_from_path(
        cls: Type[C],
        path: IntoPath,
        encoding: str = DEFAULT_ENCODING,
        errors: str = DEFAULT_ERRORS,
        ignore_sensitive: bool = DEFAULT_IGNORE_SENSITIVE,
    ) -> C:
        return cls.unsafe_from_string(
            Path(path).read_text(encoding, errors), ignore_sensitive=ignore_sensitive
        )

    @classmethod
    def unsafe_from_data(
        cls: Type[C], data: AnyConfigData, ignore_sensitive: bool = DEFAULT_IGNORE_SENSITIVE
    ) -> C:
        config_data = data.melody.expect(EXPECTED_MELODY)

        email_data = config_data.email.expect(EXPECTED_MELODY_EMAIL)

        email = EmailConfig(
            host=email_data.host.expect(EXPECTED_MELODY_EMAIL_HOST),
            port=email_data.port.expect(EXPECTED_MELODY_EMAIL_PORT),
            support=email_data.support.expect(EXPECTED_MELODY_EMAIL_SUPPORT),
            name=(
                email_data.name.unwrap_or(EMPTY)
                if ignore_sensitive
                else email_data.name.expect(EXPECTED_MELODY_EMAIL_NAME)
            ),
            password=(
                email_data.password.unwrap_or(EMPTY)
                if ignore_sensitive
                else email_data.password.expect(EXPECTED_MELODY_EMAIL_PASSWORD)
            ),
        )

        hash_data = config_data.hash.expect(EXPECTED_MELODY_HASH)

        hash = HashConfig(
            time_cost=hash_data.time_cost.expect(EXPECTED_MELODY_HASH_TIME_COST),
            memory_cost=hash_data.memory_cost.expect(EXPECTED_MELODY_HASH_MEMORY_COST),
            parallelism=hash_data.parallelism.expect(EXPECTED_MELODY_HASH_PARALLELISM),
        )

        kit_data = config_data.kit.expect(EXPECTED_MELODY_KIT)

        kit = KitConfig(
            host=kit_data.host.expect(EXPECTED_MELODY_KIT_HOST),
            port=kit_data.port.expect(EXPECTED_MELODY_KIT_PORT),
        )

        link_data = config_data.link.expect(EXPECTED_MELODY_LINK)

        link = LinkConfig(
            cache=link_data.cache.map(Path).expect(EXPECTED_MELODY_LINK_CACHE),
            error_correction=link_data.error_correction.map(ErrorCorrection).expect(
                EXPECTED_MELODY_LINK_ERROR_CORRECTION
            ),
            box_size=link_data.box_size.expect(EXPECTED_MELODY_LINK_BOX_SIZE),
            border=link_data.border.expect(EXPECTED_MELODY_LINK_BORDER),
        )

        log_data = config_data.log.expect(EXPECTED_MELODY_LOG)

        log = LogConfig(level=log_data.level.expect(EXPECTED_MELODY_LOG_LEVEL))

        redis_data = config_data.redis.expect(EXPECTED_MELODY_REDIS)

        redis = RedisConfig(
            host=redis_data.host.expect(EXPECTED_MELODY_REDIS_HOST),
            port=redis_data.port.expect(EXPECTED_MELODY_REDIS_PORT),
        )

        token_data = config_data.token.expect(EXPECTED_MELODY_TOKEN)
        expires_data = token_data.expires.expect(EXPECTED_MELODY_TOKEN_EXPIRES)

        token = TokenConfig(
            size=token_data.size.expect(EXPECTED_MELODY_TOKEN_SIZE),
            type=token_data.type.expect(EXPECTED_MELODY_TOKEN_TYPE),
            expires=ExpiresConfig(
                years=expires_data.years.expect(EXPECTED_MELODY_TOKEN_EXPIRES_YEARS),
                months=expires_data.months.expect(EXPECTED_MELODY_TOKEN_EXPIRES_MONTHS),
                weeks=expires_data.weeks.expect(EXPECTED_MELODY_TOKEN_EXPIRES_WEEKS),
                days=expires_data.days.expect(EXPECTED_MELODY_TOKEN_EXPIRES_DAYS),
                hours=expires_data.hours.expect(EXPECTED_MELODY_TOKEN_EXPIRES_HOURS),
                minutes=expires_data.minutes.expect(EXPECTED_MELODY_TOKEN_EXPIRES_MINUTES),
                seconds=expires_data.seconds.expect(EXPECTED_MELODY_TOKEN_EXPIRES_SECONDS),
            ),
        )

        web_data = config_data.web.expect(EXPECTED_MELODY_WEB)

        web = WebConfig(
            host=web_data.host.expect(EXPECTED_MELODY_WEB_HOST),
            port=web_data.port.expect(EXPECTED_MELODY_WEB_PORT),
        )

        bot_data = config_data.bot.expect(EXPECTED_MELODY_BOT)

        bot = BotConfig(
            token=(
                bot_data.token.unwrap_or(EMPTY)
                if ignore_sensitive
                else bot_data.token.expect(EXPECTED_MELODY_BOT_TOKEN)
            ),
        )

        name = config_data.name.expect(EXPECTED_MELODY_NAME)
        domain = config_data.domain.expect(EXPECTED_MELODY_DOMAIN)
        open = config_data.open.expect(EXPECTED_MELODY_OPEN)
        images = config_data.images.map(Path).expect(EXPECTED_MELODY_IMAGES)

        return cls(
            name=name,
            domain=domain,
            open=open,
            images=images,
            email=email,
            hash=hash,
            kit=kit,
            link=link,
            log=log,
            redis=redis,
            token=token,
            web=web,
            bot=bot,
        )


def get_default_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> Config:
    return Config.unsafe_from_path(
        DEFAULT_PATH, encoding=encoding, errors=errors, ignore_sensitive=True
    ).ensure_directories()


DEFAULT_CONFIG = get_default_config()


def get_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> Config:
    return Config.from_path(PATH, encoding=encoding, errors=errors).ensure_directories()
