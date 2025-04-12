pub(crate) mod import {
    pub use std::collections::HashMap;
}

macro_rules! arguments {
    ($($name: ident => $value: expr),* $(,)?) => {
        $crate::macros::import::HashMap::from([
            $(
                (stringify!($name), $value.into()),
            )*
        ])
    };
}

pub(crate) use arguments;

macro_rules! include_query {
    ($path: literal) => {
        include_str!(concat!("queries/", $path, ".edgeql"))
    };
}

pub(crate) use include_query;
