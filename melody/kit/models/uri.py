from typing_extensions import TypedDict as Data

__all__ = ("URIData",)


class URIData(Data):
    uri: str
