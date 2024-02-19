from typing import AsyncIterator, Optional
from uuid import UUID

from melody.kit.core import redis
from melody.kit.verification.factories import (
    verification_code_factory,
    verification_expires_in_factory,
)
from melody.kit.verification.keys import key_verification_code, verification_code_key
from melody.shared.constants import STAR
from melody.shared.date_time import unstructure_duration

__all__ = (
    "generate_verification_code_for",
    "delete_verification_code",
    "delete_verification_codes_for",
    "fetch_user_id_by_verification_code",
    "fetch_verification_codes_for",
)


async def generate_verification_code_for(user_id: UUID) -> str:
    verification_code = verification_code_factory()

    verification_expires = unstructure_duration(verification_expires_in_factory())

    verification_code_key_string = verification_code_key(verification_code)

    await redis.set(verification_code_key_string, str(user_id))

    if verification_expires:
        await redis.expire(verification_code_key_string, verification_expires)

    return verification_code


async def delete_verification_code(verification_code: str) -> None:
    await redis.delete(verification_code_key(verification_code))


async def delete_verification_codes_for(user_id: UUID) -> None:
    async for verification_code in fetch_verification_codes_for(user_id):
        await delete_verification_code(verification_code)


async def fetch_user_id_by_verification_code(verification_code: str) -> Optional[UUID]:
    option = await redis.get(verification_code_key(verification_code))

    return None if option is None else UUID(option)


async def fetch_verification_codes_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(verification_code_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            verification_code = key_verification_code(key)

            if verification_code is None:
                continue

            yield verification_code
