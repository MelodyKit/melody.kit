use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Port};

pub const DEFAULT_HOST: CowStr<'static> = const_borrowed_str!("127.0.0.1");
pub const DEFAULT_PORT: Port = 4269;
pub const DEFAULT_PATH: CowStr<'static> = const_borrowed_str!("static");

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Web<'w> {
    #[builder(default = DEFAULT_HOST)]
    pub host: CowStr<'w>,
    #[builder(default = DEFAULT_PORT)]
    pub port: Port,
    #[builder(default = DEFAULT_PATH)]
    pub path: CowStr<'w>,
}

impl IntoStatic for Web<'_> {
    type Static = Web<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static {
            host: self.host.into_static(),
            port: self.port,
            path: self.path.into_static(),
        }
    }
}

impl_default_with_builder!(Web<'_>);
