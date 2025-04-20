use into_static::IntoStatic;
use miette::Diagnostic;
use serde::{Deserialize, Deserializer, Serialize, Serializer, de};
use thiserror::Error;

#[derive(Debug, Error, Diagnostic)]
#[error("expected non-empty data")]
#[diagnostic(code(melody::vec), help("make sure the data is not empty"))]
pub struct Empty;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct NonEmpty<T> {
    data: Vec<T>,
}

impl<T: Serialize> Serialize for NonEmpty<T> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        self.data.serialize(serializer)
    }
}

impl<'de, T: Deserialize<'de>> Deserialize<'de> for NonEmpty<T> {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let data = Vec::deserialize(deserializer)?;

        Self::new(data).map_err(de::Error::custom)
    }
}

impl<T> NonEmpty<T> {
    pub fn new(data: Vec<T>) -> Result<Self, Empty> {
        if data.is_empty() {
            Err(Empty)
        } else {
            Ok(unsafe { Self::new_unchecked(data) })
        }
    }

    pub const unsafe fn new_unchecked(data: Vec<T>) -> Self {
        Self { data }
    }
}

impl<T: IntoStatic> IntoStatic for NonEmpty<T> {
    type Static = NonEmpty<T::Static>;

    fn into_static(self) -> Self::Static {
        // SAFETY: `IntoStatic` implementation for `Vec<T>` does not change the length
        unsafe { Self::Static::new_unchecked(self.data.into_static()) }
    }
}
