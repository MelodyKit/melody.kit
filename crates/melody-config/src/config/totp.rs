use bon::Builder;
use otp_std::{Digits, Period, Skew};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_DIGITS: Digits = Digits::DEFAULT;
pub const DEFAULT_SKEW: Skew = Skew::DEFAULT;
pub const DEFAULT_PERIOD: Period = Period::DEFAULT;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Totp {
    #[builder(default = DEFAULT_DIGITS)]
    pub digits: Digits,
    #[builder(default = DEFAULT_SKEW)]
    pub skew: Skew,
    #[builder(default = DEFAULT_PERIOD)]
    pub period: Period,
}

impl_default_with_builder!(Totp);
