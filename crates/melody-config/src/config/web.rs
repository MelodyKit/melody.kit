use std::collections::HashMap;

use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Port};

pub const DEFAULT_HOST: StaticCowStr = const_borrowed_str!("127.0.0.1");
pub const DEFAULT_PORT: Port = 4269;
pub const DEFAULT_PATH: StaticCowStr = const_borrowed_str!("static");

pub type Redirect<'r> = HashMap<CowStr<'r>, CowStr<'r>>;

pub type StaticRedirect = Redirect<'static>;

pub fn redirect_into_static(redirect: Redirect<'_>) -> StaticRedirect {
    redirect
        .into_iter()
        .map(|(name, content)| (name.into_static(), content.into_static()))
        .collect()
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Web<'w> {
    #[builder(default = DEFAULT_HOST)]
    pub host: CowStr<'w>,
    #[builder(default = DEFAULT_PORT)]
    pub port: Port,
    #[builder(default = DEFAULT_PATH)]
    pub path: CowStr<'w>,
    #[builder(default = Redirect::new())]
    pub redirect: Redirect<'w>,
}

pub type StaticWeb = Web<'static>;

impl IntoStatic for Web<'_> {
    type Static = StaticWeb;

    fn into_static(self) -> Self::Static {
        Self::Static {
            host: self.host.into_static(),
            port: self.port,
            path: self.path.into_static(),
            redirect: redirect_into_static(self.redirect),
        }
    }
}

impl_default_with_builder!(Web<'_>);
