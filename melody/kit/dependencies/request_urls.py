from fastapi import Depends
from fastapi.requests import Request
from typing_extensions import Annotated
from yarl import URL

__all__ = (
    # dependencies
    "RequestURLDependency",
    # dependables
    "request_url_dependency",
)


def request_url_dependency(request: Request) -> URL:
    return URL(str(request.url))


RequestURLDependency = Annotated[URL, Depends(request_url_dependency)]
