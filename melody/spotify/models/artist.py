from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Artist", "ArtistData")


class ArtistData(EntityData):
    ...


@define()
class Artist(Entity):
    ...


CONVERTER.register_unstructure_hook(
    Artist, make_dict_unstructure_fn(Artist, CONVERTER, client_unchecked=override(omit=True))
)
