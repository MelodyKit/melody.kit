use serde::{Deserialize, Serialize};
use strum::{AsRefStr, Display, EnumCount, EnumIs, EnumIter, EnumString, IntoStaticStr};

#[derive(
    Debug,
    Clone,
    Copy,
    PartialEq,
    Eq,
    Hash,
    AsRefStr,
    Display,
    EnumCount,
    EnumIs,
    EnumIter,
    EnumString,
    IntoStaticStr,
    Serialize,
    Deserialize,
)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
pub enum EntityType {
    Track,
    Artist,
    Album,
    Playlist,
    User,
}

#[derive(
    Debug,
    Clone,
    Copy,
    PartialEq,
    Eq,
    Hash,
    Default,
    Display,
    AsRefStr,
    EnumCount,
    EnumIs,
    EnumIter,
    EnumString,
    IntoStaticStr,
    Serialize,
    Deserialize,
)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
pub enum AlbumType {
    #[default]
    Album,
    Single,
    Compilation,
}
