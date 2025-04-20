use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_NAME: StaticCowStr = const_borrowed_str!("MelodyKit");
pub const DEFAULT_DOMAIN: StaticCowStr = const_borrowed_str!("melodykit.app");
pub const DEFAULT_OPEN: StaticCowStr = const_borrowed_str!("open");
pub const DEFAULT_DOCS: StaticCowStr = const_borrowed_str!("docs");
pub const DEFAULT_API: StaticCowStr = const_borrowed_str!("api");
pub const DEFAULT_DEV: StaticCowStr = const_borrowed_str!("dev");
pub const DEFAULT_TOKEN_TYPE: StaticCowStr = const_borrowed_str!("Bearer");

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Context<'c> {
    #[builder(default = DEFAULT_NAME)]
    pub name: CowStr<'c>,

    #[builder(default = DEFAULT_DOMAIN)]
    pub domain: CowStr<'c>,

    #[builder(default = DEFAULT_OPEN)]
    pub open: CowStr<'c>,

    #[builder(default = DEFAULT_DOCS)]
    pub docs: CowStr<'c>,

    #[builder(default = DEFAULT_API)]
    pub api: CowStr<'c>,

    #[builder(default = DEFAULT_DEV)]
    pub dev: CowStr<'c>,

    #[builder(default = DEFAULT_TOKEN_TYPE)]
    pub token_type: CowStr<'c>,
}

pub type StaticContext = Context<'static>;

impl IntoStatic for Context<'_> {
    type Static = StaticContext;

    fn into_static(self) -> Self::Static {
        Self::Static {
            name: self.name.into_static(),
            domain: self.domain.into_static(),
            open: self.open.into_static(),
            docs: self.docs.into_static(),
            api: self.api.into_static(),
            dev: self.dev.into_static(),
            token_type: self.token_type.into_static(),
        }
    }
}

impl_default_with_builder!(Context<'_>);
