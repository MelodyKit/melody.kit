from attrs import Factory, frozen
from pendulum import Duration

from melody.kit.tokens.factories import (
    access_token_factory,
    expires_in_factory,
    refresh_token_factory,
    token_type_factory,
)
from melody.shared.tokens import Tokens as SharedTokens

__all__ = ("Tokens",)


@frozen()
class Tokens(SharedTokens):
    # NOTE: here we simply provide defaults to fields in `melody.shared` without them

    access_token: str = Factory(access_token_factory)
    expires_in: Duration = Factory(expires_in_factory)
    token_type: str = Factory(token_type_factory)
    refresh_token: str = Factory(refresh_token_factory)
