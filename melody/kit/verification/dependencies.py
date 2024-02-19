from uuid import UUID

from attrs import frozen
from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.kit.errors.auth import AuthVerificationCodeInvalid
from melody.kit.verification.operations import fetch_user_id_by_verification_code

__all__ = (
    # types
    "BoundVerificationCode",
    # dependencies
    "BoundVerificationCodeDependency",
    "VerificationCodeDependency",
    # dependables
    "bound_verification_code_dependency",
    "verification_code_dependency",
)


@frozen()
class BoundVerificationCode:
    code: str
    user_id: UUID


FormVerificationCodeDependency = Annotated[str, Form()]


async def bound_verification_code_dependency(
    verification_code: FormVerificationCodeDependency,
) -> BoundVerificationCode:
    user_id = await fetch_user_id_by_verification_code(verification_code)

    if user_id is None:
        raise AuthVerificationCodeInvalid()

    return BoundVerificationCode(verification_code, user_id)


BoundVerificationCodeDependency = Annotated[
    BoundVerificationCode, Depends(bound_verification_code_dependency)
]


async def verification_code_dependency(
    bound_verification_code: BoundVerificationCodeDependency,
) -> UUID:
    return bound_verification_code.user_id


VerificationCodeDependency = Annotated[UUID, Depends(verification_code_dependency)]
