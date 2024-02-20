from typing import Optional
from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.shared.tokens import Scopes

__all__ = (
    # dependencies
    "ScopesDependency",
    # dependables
    "scopes_dependency",
)

OptionalScopeDependency = Annotated[Optional[str], Form()]


def scopes_dependency(scope: OptionalScopeDependency = None) -> Scopes:
    return Scopes() if scope is None else Scopes.from_scope(scope)


ScopesDependency = Annotated[Scopes, Depends(scopes_dependency)]
