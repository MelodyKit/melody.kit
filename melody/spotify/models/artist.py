from attrs import define

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Artist", "ArtistData")


class ArtistData(EntityData):
    ...


@register_unstructure_hook_omit_client
@define()
class Artist(Entity):
    ...
