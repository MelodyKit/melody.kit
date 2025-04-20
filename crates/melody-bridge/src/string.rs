use std::borrow::Cow;

use non_empty_str::{CowStr, Empty, OwnedStr, Str};

use crate::bridge::TryBridge;

impl TryBridge for String {
    type Model = OwnedStr;
    type Error = Empty;

    fn try_bridge(self) -> Result<OwnedStr, Self::Error> {
        OwnedStr::new(self)
    }
}

impl<'s> TryBridge for &'s str {
    type Model = Str<'s>;
    type Error = Empty;

    fn try_bridge(self) -> Result<Str<'s>, Self::Error> {
        Str::new(self)
    }
}

impl<'s> TryBridge for Cow<'s, str> {
    type Model = CowStr<'s>;
    type Error = Empty;

    fn try_bridge(self) -> Result<CowStr<'s>, Self::Error> {
        CowStr::new(self)
    }
}
