from typing import Optional

from fastapi import Form
from typing_extensions import Annotated

__all__ = ("CodeDependency", "OptionalCodeDependency")

CodeDependency = Annotated[str, Form()]
OptionalCodeDependency = Annotated[Optional[str], Form()]
