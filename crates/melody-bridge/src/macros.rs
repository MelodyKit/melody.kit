pub(crate) mod import {
    pub use miette::Diagnostic;
    pub use non_empty_str::Empty;
    pub use paste::paste;
    pub use thiserror::Error;
}

macro_rules! empty_error {
    ($vis: vis $name: ident @ $string: expr => $doc: expr) => {
        $crate::macros::import::paste! {
            #[doc = concat!("Represents errors that occur when the ", $doc, " is empty.")]
            #[derive(Debug, $crate::macros::import::Error, $crate::macros::import::Diagnostic)]
            #[error("empty {string} received", string = $string)]
            #[diagnostic(code(melody::bridge::[< $name:snake >]::empty), help("make sure the {string} is non-empty", string = $string))]
            $vis struct [< Empty $name Error >](#[from] pub $crate::macros::import::Empty);
        }
    };
}

pub(crate) use empty_error;
