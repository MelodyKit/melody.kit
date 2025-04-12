use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_NAME: CowStr<'static> = const_borrowed_str!("MelodyKit");
pub const DEFAULT_DOMAIN: CowStr<'static> = const_borrowed_str!("melodykit.app");
pub const DEFAULT_OPEN: CowStr<'static> = const_borrowed_str!("open");
pub const DEFAULT_TOKEN_TYPE: CowStr<'static> = const_borrowed_str!("Bearer");

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Context<'c> {
    #[builder(default = DEFAULT_NAME)]
    pub name: CowStr<'c>,

    #[builder(default = DEFAULT_DOMAIN)]
    pub domain: CowStr<'c>,

    #[builder(default = DEFAULT_OPEN)]
    pub open: CowStr<'c>,

    #[builder(default = DEFAULT_TOKEN_TYPE)]
    pub token_type: CowStr<'c>,
}

impl IntoStatic for Context<'_> {
    type Static = Context<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .name(self.name.into_static())
            .domain(self.domain.into_static())
            .open(self.open.into_static())
            .token_type(self.token_type.into_static())
            .build()
    }
}

impl_default_with_builder!(Context<'_>);
