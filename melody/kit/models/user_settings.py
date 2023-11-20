from typing import Type, TypeVar, overload

from attrs import define
from edgedb import Object  # type: ignore
from typing_extensions import TypedDict as Data

from melody.kit.constants import DEFAULT_AUTOPLAY, DEFAULT_EXPLICIT
from melody.kit.enums import Platform, PrivacyType
from melody.shared.converter import CONVERTER

__all__ = (
    "UserSettings",
    "UserSettingsData",
    "user_settings_from_object",
    "user_settings_from_data",
    "user_settings_into_data",
)


class UserSettingsData(Data):
    name: str

    explicit: bool

    autoplay: bool

    platform: str

    privacy_type: str


US = TypeVar("US", bound="UserSettings")


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
    def from_object(cls: Type[US], object: Object) -> US:  # type: ignore
        return cls(
            name=object.name,
            explicit=object.explicit,
            autoplay=object.autoplay,
            platform=Platform(object.platform.value),
            privacy_type=PrivacyType(object.privacy_type.value),
        )

    @classmethod
    def from_data(cls: Type[US], data: UserSettingsData) -> US:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserSettingsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_settings_from_object(object: Object) -> UserSettings:  # type: ignore
    ...


@overload
def user_settings_from_object(object: Object, user_settings_type: Type[US]) -> US:  # type: ignore
    ...


def user_settings_from_object(
    object: Object, user_settings_type: Type[UserSettings] = UserSettings  # type: ignore
) -> UserSettings:
    return user_settings_type.from_object(object)


@overload
def user_settings_from_data(data: UserSettingsData) -> UserSettings:
    ...


@overload
def user_settings_from_data(data: UserSettingsData, user_settings_type: Type[US]) -> US:
    ...


def user_settings_from_data(
    data: UserSettingsData, user_settings_type: Type[UserSettings] = UserSettings
) -> UserSettings:
    return user_settings_type.from_data(data)


def user_settings_into_data(user_settings: UserSettings) -> UserSettingsData:
    return user_settings.into_data()
