from secrets import token_hex
from typing import AsyncIterator, Optional
from uuid import UUID

from attrs import define
from fastapi import Depends, Form
from pendulum import Duration
from typing_extensions import Annotated

from melody.kit.core import config, redis
from melody.kit.errors import AuthInvalid
from melody.shared.constants import NAME_SEPARATOR, STAR, VERIFICATION_CODE

__all__ = (
    "BoundVerificationCode",
    "verification_code_factory",
    "verification_expires_in_factory",
    "generate_verification_code_for",
    "delete_verification_code",
    "delete_verification_codes_for",
    "fetch_user_id_by_verification_code",
    "fetch_verification_codes_for",
    "bound_verification_code_dependency",
    "verification_code_dependency",
)


@define()
class BoundVerificationCode:
    code: str
    self_id: UUID


def verification_code_factory() -> str:
    return token_hex(config.verification.size)


def verification_expires_in_factory() -> Duration:
    return config.verification.expires.duration


VERIFICATION_CODE_KEY = f"{VERIFICATION_CODE}{NAME_SEPARATOR}{{}}"
verification_code_key = VERIFICATION_CODE_KEY.format


def key_verification_code(key: str) -> Optional[str]:
    _, _, verification_code = key.partition(NAME_SEPARATOR)

    return verification_code if verification_code else None


async def generate_verification_code_for(user_id: UUID) -> str:
    verification_code = verification_code_factory()

    verification_expires = int(verification_expires_in_factory().total_seconds())

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


async def fetch_user_id_by_verification_code(
    verification_code: str,
) -> Optional[UUID]:
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


INVALID_VERIFICATION_CODE = "verification code `{}` is invalid"
invalid_verification_code = INVALID_VERIFICATION_CODE.format


FormVerificationCodeDependency = Annotated[str, Form()]


async def bound_verification_code_dependency(
    verification_code: FormVerificationCodeDependency,
) -> BoundVerificationCode:
    self_id = await fetch_user_id_by_verification_code(verification_code)

    if self_id is None:
        raise AuthInvalid(invalid_verification_code(verification_code))

    return BoundVerificationCode(verification_code, self_id)


BoundVerificationCodeDependency = Annotated[
    BoundVerificationCode, Depends(bound_verification_code_dependency)
]


async def verification_code_dependency(
    bound_verification_code: BoundVerificationCodeDependency,
) -> UUID:
    return bound_verification_code.self_id


VerificationCodeDependency = Annotated[UUID, Depends(verification_code_dependency)]
