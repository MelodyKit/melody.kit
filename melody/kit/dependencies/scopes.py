from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.shared.tokens import Scopes

__all__ = (
    # dependencies
    "ScopesDependency",
    # dependables
    "scopes_dependency",
)

FormScopeDependency = Annotated[str, Form()]


def scopes_dependency(scope: FormScopeDependency) -> Scopes:
    return Scopes.from_scope(scope)


ScopesDependency = Annotated[Scopes, Depends(scopes_dependency)]
