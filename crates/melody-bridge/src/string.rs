use std::borrow::Cow;

use non_empty_str::{CowStr, Empty, StaticCowStr};

use crate::bridge::TryBridge;

impl TryBridge for String {
    type Model = StaticCowStr;
    type Error = Empty;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        Self::Model::owned(self)
    }
}

impl<'s> TryBridge for &'s str {
    type Model = CowStr<'s>;
    type Error = Empty;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        Self::Model::borrowed(self)
    }
}

impl<'s> TryBridge for Cow<'s, str> {
    type Model = CowStr<'s>;
    type Error = Empty;

    fn try_bridge(self) -> Result<CowStr<'s>, Self::Error> {
        Self::Model::new(self)
    }
}
