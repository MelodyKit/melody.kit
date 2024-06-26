from typing import final

from attrs import frozen
from keyring import get_password
from typing_extensions import Self

from melody.kit.config.core import CONFIG, Config
from melody.shared.constants import CREDENTIALS_SEPARATOR

__all__ = ("Keyring", "KEYRING")

CAN_NOT_FIND = "can not find `{}` credentials in `{}`"
can_not_find = CAN_NOT_FIND.format


class FindKeyringCredentialsError(LookupError):
    def __init__(self, name: str, service_name: str) -> None:
        self._name = name
        self._service_name = service_name

        super().__init__(can_not_find(name, service_name))

    @property
    def name(self) -> str:
        return self._name

    @property
    def service_name(self) -> str:
        return self._service_name


def find_keyring_credentials(service_name: str, name: str) -> str:
    result = get_password(service_name, name)

    if result is None:
        raise FindKeyringCredentialsError(name, service_name)

    return result


@final
@frozen()
class KeyringEmailCredentials:
    username: str
    password: str


CAN_NOT_PARSE_EMAIL_CREDENTIALS = "can not parse `{}` email credentials"
can_not_parse_email_credentials = CAN_NOT_PARSE_EMAIL_CREDENTIALS.format


class ParseKeyringEmailCredentialsError(ValueError):
    def __init__(self, name: str) -> None:
        self._name = name

        super().__init__(can_not_parse_email_credentials(name))

    @property
    def name(self) -> str:
        return self._name


def parse_keyring_email_credentials(string: str, name: str) -> KeyringEmailCredentials:
    username, separator, password = string.partition(CREDENTIALS_SEPARATOR)

    if not separator:
        raise ParseKeyringEmailCredentialsError(name)

    return KeyringEmailCredentials(username, password)


@final
@frozen()
class KeyringClientCredentials:
    id: str
    secret: str


CAN_NOT_PARSE_CLIENT_CREDENTIALS = "can not parse `{}` client credentials"
can_not_parse_client_credentials = CAN_NOT_PARSE_CLIENT_CREDENTIALS.format


class ParseKeyringClientCredentialsError(ValueError):
    def __init__(self, name: str) -> None:
        self._name = name

        super().__init__(can_not_parse_client_credentials(name))

    @property
    def name(self) -> str:
        return self._name


def parse_keyring_client_credentials(string: str, name: str) -> KeyringClientCredentials:
    id, separator, secret = string.partition(CREDENTIALS_SEPARATOR)

    if not separator:
        raise ParseKeyringClientCredentialsError(name)

    return KeyringClientCredentials(id, secret)


@final
@frozen()
class Keyring:
    session: str
    bot: str
    email: KeyringEmailCredentials
    discord: KeyringClientCredentials
    spotify: KeyringClientCredentials

    @classmethod
    def from_config(cls, config: Config) -> Self:
        keyring_config = config.keyring

        service_name = keyring_config.name

        session_name = keyring_config.session
        bot_name = keyring_config.bot

        session = find_keyring_credentials(service_name, session_name)
        bot = find_keyring_credentials(service_name, bot_name)

        email_name = keyring_config.email

        email = parse_keyring_email_credentials(
            find_keyring_credentials(service_name, email_name), email_name
        )

        discord_name = keyring_config.discord
        spotify_name = keyring_config.spotify

        discord = parse_keyring_client_credentials(
            find_keyring_credentials(service_name, discord_name), discord_name
        )
        spotify = parse_keyring_client_credentials(
            find_keyring_credentials(service_name, spotify_name), spotify_name
        )

        return cls(session=session, bot=bot, email=email, discord=discord, spotify=spotify)


KEYRING = Keyring.from_config(CONFIG)
