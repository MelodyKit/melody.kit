from pathlib import Path
from typing import Any, Type, TypeVar, cast

from attrs import define
from toml import loads as load_string
from wraps import Option, wrap_optional

from melody.kit.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, DEFAULT_IGNORE_KEY, EMPTY
from melody.kit.typing import IntoPath, StringDict

__all__ = ("Config", "ConfigData", "get_config")

T = TypeVar("T")

HOME = Path.home()

CONFIG_NAME = ".config"
MELODY_NAME = "melody"

NAME = "kit.toml"

DEFAULT_PATH = Path(__file__).parent.parent / NAME
PATH = HOME / CONFIG_NAME / MELODY_NAME / NAME


class ConfigData(StringDict[T]):
    def __getattr__(self, name: str) -> Option[T]:
        return wrap_optional(self.get(name))


AnyConfigData = ConfigData[Any]


@define()
class HashConfig:
    time_cost: int
    memory_cost: int
    parallelism: int


@define()
class KitConfig:
    host: str
    port: int
    key: str


EXPECTED = "expected `{}`"
expected = EXPECTED.format


EXPECTED_MELODY = expected("melody")
EXPECTED_MELODY_HASH = expected("melody.hash")
EXPECTED_MELODY_HASH_TIME_COST = expected("melody.hash.time_cost")
EXPECTED_MELODY_HASH_MEMORY_COST = expected("melody.hash.memory_cost")
EXPECTED_MELODY_HASH_PARALLELISM = expected("melody.hash.parallelism")
EXPECTED_MELODY_KIT = expected("melody.kit")
EXPECTED_MELODY_KIT_HOST = expected("melody.kit.host")
EXPECTED_MELODY_KIT_PORT = expected("melody.kit.port")
EXPECTED_MELODY_KIT_KEY = expected("melody.kit.key")


C = TypeVar("C", bound="Config")


@define()
class Config:
    hash: HashConfig
    kit: KitConfig

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
            key=kit_data.key.expect(EXPECTED_MELODY_KIT_KEY),
        )

        return cls(hash=hash, kit=kit)

    @classmethod
    def unsafe_from_string(cls: Type[C], string: str, ignore_key: bool = DEFAULT_IGNORE_KEY) -> C:
        return cls.unsafe_from_data(cls.parse(string), ignore_key=ignore_key)

    @classmethod
    def unsafe_from_path(
        cls: Type[C],
        path: IntoPath,
        encoding: str = DEFAULT_ENCODING,
        errors: str = DEFAULT_ERRORS,
        ignore_key: bool = DEFAULT_IGNORE_KEY,
    ) -> C:
        return cls.unsafe_from_string(Path(path).read_text(encoding, errors), ignore_key=ignore_key)

    @classmethod
    def unsafe_from_data(
        cls: Type[C], data: AnyConfigData, ignore_key: bool = DEFAULT_IGNORE_KEY
    ) -> C:
        config_data = data.melody.expect(EXPECTED_MELODY)

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
            key=(
                kit_data.key.unwrap_or(EMPTY)
                if ignore_key
                else kit_data.key.expect(EXPECTED_MELODY_KIT_KEY)
            ),
        )

        return cls(hash=hash, kit=kit)


DEFAULT_CONFIG = Config.unsafe_from_path(DEFAULT_PATH, ignore_key=True)


def ensure_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> None:
    if not PATH.exists():
        PATH.parent.mkdir(parents=True, exist_ok=True)

        PATH.write_text(DEFAULT_PATH.read_text(encoding, errors), encoding, errors)


ensure_config()


def get_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> Config:
    return Config.from_path(PATH)
