from uuid import UUID

from yarl import URL

from melody.kit.totp.core import create_totp
from melody.shared.constants import CODE_TYPE, SECRET

__all__ = ("provisioning_url", "provisioning_code_name")


def provisioning_url(user_id: UUID, secret: str) -> URL:
    totp = create_totp(secret)

    uri = totp.provisioning_uri(name=str(user_id))

    url = URL(uri)

    return url


PROVISIONING_CODE_NAME = f"{SECRET}.{{}}.{CODE_TYPE}"
provisioning_code_name = PROVISIONING_CODE_NAME.format
