use bon::Builder;
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Unit};

pub const DEFAULT_YEARS: Unit = 0;
pub const DEFAULT_MONTHS: Unit = 0;
pub const DEFAULT_WEEKS: Unit = 0;
pub const DEFAULT_DAYS: Unit = 0;
pub const DEFAULT_HOURS: Unit = 0;
pub const DEFAULT_MINUTES: Unit = 0;
pub const DEFAULT_SECONDS: Unit = 0;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Expires {
    #[builder(default = DEFAULT_YEARS)]
    pub years: Unit,
    #[builder(default = DEFAULT_MONTHS)]
    pub months: Unit,
    #[builder(default = DEFAULT_WEEKS)]
    pub weeks: Unit,
    #[builder(default = DEFAULT_DAYS)]
    pub days: Unit,
    #[builder(default = DEFAULT_HOURS)]
    pub hours: Unit,
    #[builder(default = DEFAULT_MINUTES)]
    pub minutes: Unit,
    #[builder(default = DEFAULT_SECONDS)]
    pub seconds: Unit,
}

impl_default_with_builder!(Expires);

pub const DEFAULT_VERIFICATION_SIZE: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Verification {
    #[builder(default)]
    pub expires: Expires,
    #[builder(default = DEFAULT_VERIFICATION_SIZE)]
    pub size: usize,
}

impl_default_with_builder!(Verification);

pub const DEFAULT_AUTHORIZATION_SIZE: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Authorization {
    #[builder(default)]
    pub expires: Expires,
    #[builder(default = DEFAULT_AUTHORIZATION_SIZE)]
    pub size: usize,
}

impl_default_with_builder!(Authorization);

pub const DEFAULT_ACCESS_SIZE: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Access {
    #[builder(default)]
    pub expires: Expires,
    #[builder(default = DEFAULT_ACCESS_SIZE)]
    pub size: usize,
}

impl_default_with_builder!(Access);

pub const DEFAULT_REFRESH_SIZE: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Refresh {
    #[builder(default)]
    pub expires: Expires,
    #[builder(default = DEFAULT_REFRESH_SIZE)]
    pub size: usize,
}

impl_default_with_builder!(Refresh);
