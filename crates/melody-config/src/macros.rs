//! Macros for implementing [`FromPath`] via loading TOML files.
//!
//! [`FromPath`]: from_path::FromPath

#[allow(unused_imports)]
#[doc(hidden)]
pub mod import {
    pub use std::{convert::AsRef, path::Path};

    pub use from_path::FromPath;
}

#[macro_export]
macro_rules! impl_from_path_with_toml {
    ($type: ty) => {
        impl $crate::macros::import::FromPath for $type {
            type Error = $crate::load::Error;

            fn from_path<P: $crate::macros::import::AsRef<$crate::macros::import::Path>>(
                path: P,
            ) -> Result<Self, Self::Error> {
                $crate::load::load(path)
            }
        }
    };
}

#[macro_export]
macro_rules! impl_default_with_builder {
    ($type: ty) => {
        impl Default for $type {
            fn default() -> Self {
                Self::builder().build()
            }
        }
    };
}
