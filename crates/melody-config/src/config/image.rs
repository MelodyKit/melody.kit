use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_DIRECTORY: StaticCowStr = const_borrowed_str!("~/.melody/kit/images");
pub const DEFAULT_DATA_LIMIT: usize = 16777216;
pub const DEFAULT_SIZE_LIMIT: usize = 4096;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Image<'i> {
    #[builder(default = DEFAULT_DIRECTORY)]
    pub directory: CowStr<'i>,
    #[builder(default = DEFAULT_DATA_LIMIT)]
    pub data_limit: usize,
    #[builder(default = DEFAULT_SIZE_LIMIT)]
    pub size_limit: usize,
}

pub type StaticImage = Image<'static>;

impl IntoStatic for Image<'_> {
    type Static = StaticImage;

    fn into_static(self) -> Self::Static {
        Self::Static {
            directory: self.directory.into_static(),
            data_limit: self.data_limit,
            size_limit: self.size_limit,
        }
    }
}

impl_default_with_builder!(Image<'_>);
