use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Port};

pub const DEFAULT_HOST: StaticCowStr = const_borrowed_str!("smtp.gmail.com");
pub const DEFAULT_PORT: Port = 587;
pub const DEFAULT_SUPPORT: StaticCowStr = const_borrowed_str!("support");

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Email<'e> {
    #[builder(default = DEFAULT_HOST)]
    pub host: CowStr<'e>,

    #[builder(default = DEFAULT_PORT)]
    pub port: Port,

    #[builder(default = DEFAULT_SUPPORT)]
    pub support: CowStr<'e>,
}

pub type StaticEmail = Email<'static>;

impl IntoStatic for Email<'_> {
    type Static = StaticEmail;

    fn into_static(self) -> Self::Static {
        Self::Static {
            host: self.host.into_static(),
            port: self.port,
            support: self.support.into_static(),
        }
    }
}

impl_default_with_builder!(Email<'_>);
