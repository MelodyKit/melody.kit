from attrs import define
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Track", "TrackData")


class TrackData(EntityData):
    ...


@define()
class Track(Entity):
    ...
