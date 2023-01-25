from uuid import UUID

from fastapi import status

from melody.kit.core import database, v1, verification_tokens
from melody.kit.errors import Error, ErrorCode

__all__ = ("verify",)

VERIFICATION_TOKEN_MISMATCH = "verification token mismatch"
VERIFICATION_NOT_FOUND = "verification for the user with id `{}` not found"


@v1.get("/verify/{user_id}/{verification_token}")
async def verify(user_id: UUID, verification_token: str) -> None:
    if user_id in verification_tokens:
        if verification_tokens[user_id] == verification_token:
            del verification_tokens[user_id]

            await database.update_user_verified(user_id, True)

        else:
            raise Error(
                VERIFICATION_TOKEN_MISMATCH, ErrorCode.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED
            )

    else:
        raise Error(
            VERIFICATION_NOT_FOUND.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )
