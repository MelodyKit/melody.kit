from yarl import URL

from melody.kit.connections import callback_url
from melody.kit.core import config
from melody.kit.enums import Connection
from melody.shared.constants import CODE

__all__ = ("AUTHORIZE_URL", "authorize_url")

AUTHORIZE_URL = URL("https://discord.com/oauth2/authorize")

SCOPE = "identify"


def authorize_url(state: str, scope: str = SCOPE) -> URL:
    return AUTHORIZE_URL.with_query(
        client_id=config.discord.client_id,
        state=state,
        scope=scope,
        response_type=CODE,
        redirect_uri=str(callback_url(Connection.DISCORD)),
    )
