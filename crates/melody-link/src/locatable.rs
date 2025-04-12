use crate::uri::Uri;

pub trait Locatable {
    fn uri(&self) -> Uri;
}
