use non_empty_str::{CowStr, Empty};

pub const fn borrowed_from_schema(string: &str) -> Result<CowStr<'_>, Empty> {
    CowStr::borrowed(string)
}

pub fn owned_from_schema(string: String) -> Result<CowStr<'static>, Empty> {
    CowStr::owned(string)
}
