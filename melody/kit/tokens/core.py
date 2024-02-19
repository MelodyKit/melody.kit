from attrs import define, field
from pendulum import Duration

from melody.kit.tokens.factories import (
    access_token_factory,
    expires_in_factory,
    refresh_token_factory,
    token_type_factory,
)
from melody.shared.tokens import Tokens as SharedTokens

__all__ = ("Tokens",)


@define()
class Tokens(SharedTokens):
    # NOTE: here we simply provide defaults to fields in `melody.shared` without them

    access_token: str = field(factory=access_token_factory)
    expires_in: Duration = field(factory=expires_in_factory)
    token_type: str = field(factory=token_type_factory)
    refresh_token: str = field(factory=refresh_token_factory)
