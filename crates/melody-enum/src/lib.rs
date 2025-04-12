#[doc(hidden)]
pub mod import {
    pub use std::{convert::AsRef, fmt, result::Result, str::FromStr, string::String};

    pub use miette::Diagnostic;
    pub use paste::paste;
    pub use serde::{Deserialize, Deserializer, Serialize, Serializer, de};
    pub use thiserror::Error;

    pub type Str<'s> = &'s str;
    pub type StaticStr = Str<'static>;
}

#[macro_export]
macro_rules! melody_enum {
    (
        $(#[$meta: meta])*
        $vis: vis $name: ident {
            $(
                $(#[$variant_meta: meta])*
                $variant: ident => $part: ident $(:: $rest: ident)*,
            )*
        }
    ) => {
        $crate::import::paste! {
            #[derive(Debug, $crate::import::Error, $crate::import::Diagnostic)]
            #[error("`{code}` is not valid for `{name}`", name = stringify!($name))]
            $vis struct [< $name Error >] {
                $vis code: $crate::import::String,
            }

            impl [< $name Error >] {
                $vis const fn new(code: $crate::import::String) -> Self {
                    Self { code }
                }
            }

            $(#[$meta])*
            $vis enum $name {
                $(
                    $(#[$variant_meta])*
                    $variant,
                )*
            }

            impl $name {
                pub const fn code(self) -> $crate::import::StaticStr {
                    match self {
                        $(
                            Self::$variant => $crate::stringify_code!($part $($rest)*),
                        )*
                    }
                }
            }

            impl $crate::import::FromStr for $name {
                type Err = [< $name Error >];

                fn from_str(string: &str) -> $crate::import::Result<Self, Self::Err> {
                    match string {
                        $(
                            $crate::stringify_code!($part $($rest)*) => Ok(Self::$variant),
                        )*
                        _ => $crate::import::Result::Err(Self::Err::new(string.to_owned())),
                    }
                }
            }

            impl $crate::import::Serialize for $name {
                fn serialize<S: $crate::import::Serializer>(
                    &self, serializer: S
                ) -> Result<S::Ok, S::Error> {
                    self.code().serialize(serializer)
                }
            }

            impl<'de> $crate::import::Deserialize<'de> for $name {
                fn deserialize<D: $crate::import::Deserializer<'de>>(
                    deserializer: D,
                ) -> Result<Self, D::Error> {
                    let code = $crate::import::Str::deserialize(deserializer)?;

                    let variant = code.parse().map_err($crate::import::de::Error::custom)?;

                    Ok(variant)
                }
            }

            impl $crate::import::fmt::Display for $name {
                fn fmt(
                    &self, formatter: &mut $crate::import::fmt::Formatter<'_>
                ) -> $crate::import::fmt::Result {
                    self.code().fmt(formatter)
                }
            }

            impl From<$name> for $crate::import::StaticStr {
                fn from(value: $name) -> Self {
                    value.code()
                }
            }

            impl $crate::import::AsRef<str> for $name {
                fn as_ref(&self) -> &str {
                    self.code()
                }
            }

            impl $name {
                pub const COUNT: usize = $crate::count_names!($($variant)*);

                pub const CODES: [$crate::import::StaticStr; Self::COUNT] = [
                    $(
                        $crate::stringify_code!($part $($rest)*),
                    )*
                ];
            }

            impl $name {
                pub const ARRAY: [Self; Self::COUNT] = [
                    $(
                        Self::$variant,
                    )*
                ];
            }

            impl $name {
                $(
                    pub const fn [< is_ $variant:snake >](self) -> bool {
                        matches!(self, Self::$variant)
                    }
                )*
            }
        }
    };
}

#[doc(hidden)]
#[macro_export]
macro_rules! stringify_code {
    ($part: ident) => {
        stringify!($part)
    };

    ($part: ident $($rest: ident)+) => {
        concat!($crate::stringify_code!($part), "::", $crate::stringify_code!($($rest)+))
    };
}

#[doc(hidden)]
#[macro_export]
macro_rules! count_names {
    () => {
        0
    };

    ($name: ident $($rest: ident)*) => {
        1 + $crate::count_names!($($rest)*)
    };
}
