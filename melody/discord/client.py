from typing import Optional

from attrs import define, field
from typing_extensions import Self

from melody.discord.http import HTTPClient
from melody.discord.models.entity import Entity
from melody.kit.core import keyring
from melody.shared.tokens import Tokens

TOKENS_NOT_ATTACHED = "`tokens` not attached to the client"


def client_id_factory() -> str:
    return keyring.discord.id


def client_secret_factory() -> str:
    return keyring.discord.secret


@define()
class Client:
    client_id: str = field(factory=client_id_factory)
    client_secret: str = field(factory=client_secret_factory, repr=False)

    http: HTTPClient = field(factory=HTTPClient)

    tokens_unchecked: Optional[Tokens] = field(default=None, init=False, repr=False)

    @property
    def tokens(self) -> Tokens:
        tokens = self.tokens_unchecked

        if tokens is None:
            raise ValueError(TOKENS_NOT_ATTACHED)

        return tokens

    @tokens.setter
    def tokens(self, tokens: Tokens) -> None:
        self.tokens_unchecked = tokens

    @tokens.deleter
    def tokens(self) -> None:
        self.tokens_unchecked = None

    def attach_tokens(self, tokens: Tokens) -> Self:
        self.tokens = tokens

        return self

    def detach_tokens(self) -> Self:
        del self.tokens

        return self

    async def get_self(self) -> Entity:
        data = await self.http.get_self(tokens=self.tokens)

        return Entity.from_data(data)
