from typing import Optional, TypeVar

from attrs import define, field

from melody.spotify.http import HTTPClient
from melody.spotify.models.tokens import Tokens, tokens_from_data
from melody.spotify.models.track import Track, track_from_data

__all__ = ("Client",)

TOKENS_NOT_ATTACHED = "`tokens` not attached to the client"

C = TypeVar("C", bound="Client")


@define()
class Client:
    client_id: str = field()
    client_secret: str = field()

    tokens_unchecked: Optional[Tokens] = field(default=None)

    http: HTTPClient = field(factory=HTTPClient)

    @property
    def tokens(self) -> Tokens:
        tokens = self.tokens_unchecked

        if tokens is None:
            raise RuntimeError(TOKENS_NOT_ATTACHED)

        return tokens

    @tokens.setter
    def tokens(self, tokens: Tokens) -> None:
        self.tokens_unchecked = tokens

    @tokens.deleter
    def tokens(self) -> None:
        self.tokens_unchecked = None

    def attach_tokens(self: C, tokens: Tokens) -> C:
        self.tokens = tokens

        return self

    def detach_tokens(self: C) -> C:
        del self.tokens

        return self

    async def get_track(self, track_id: str) -> Track:
        data = await self.http.get_track(track_id, self.tokens)

        return track_from_data(data).attach_client(self)

    async def get_client_credentials(self) -> Tokens:
        data = await self.http.get_client_credentials(self.client_id, self.client_secret)

        return tokens_from_data(data)
