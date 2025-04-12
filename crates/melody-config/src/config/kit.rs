use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Port};

pub const DEFAULT_HOST: CowStr<'static> = const_borrowed_str!("127.0.0.1");
pub const DEFAULT_PORT: Port = 1342;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Kit<'k> {
    #[builder(default = DEFAULT_HOST)]
    pub host: CowStr<'k>,

    #[builder(default = DEFAULT_PORT)]
    pub port: Port,
}

impl IntoStatic for Kit<'_> {
    type Static = Kit<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .host(self.host.into_static())
            .port(self.port)
            .build()
    }
}

impl_default_with_builder!(Kit<'_>);
