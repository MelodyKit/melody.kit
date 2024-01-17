from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.constants import DEFAULT_AUTOPLAY, DEFAULT_EXPLICIT
from melody.kit.enums import Platform, PrivacyType
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("UserSettings", "UserSettingsData")


class UserSettingsData(Data):
    name: str

    explicit: bool

    autoplay: bool

    platform: str

    privacy_type: str


@define()
class UserSettings:
    name: str

    explicit: bool = DEFAULT_EXPLICIT

    autoplay: bool = DEFAULT_AUTOPLAY

    platform: Platform = Platform.DEFAULT

    privacy_type: PrivacyType = PrivacyType.DEFAULT

    def is_explicit(self) -> bool:
        return self.explicit

    def is_autoplay(self) -> bool:
        return self.autoplay

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            name=object.name,
            explicit=object.explicit,
            autoplay=object.autoplay,
            platform=Platform(object.platform.value),
            privacy_type=PrivacyType(object.privacy_type.value),
        )

    @classmethod
    def from_data(cls, data: UserSettingsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserSettingsData:
        return CONVERTER.unstructure(self)  # type: ignore
