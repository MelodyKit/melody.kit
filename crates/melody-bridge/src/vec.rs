use miette::Diagnostic;
use thiserror::Error;

use crate::bridge::{Bridge, TryBridge};

impl<T: Bridge> Bridge for Vec<T> {
    type Model = Vec<T::Model>;

    fn bridge(self) -> Self::Model {
        self.into_iter().map(Bridge::bridge).collect()
    }
}

pub fn try_bridge_one<T: TryBridge>(item: T, index: usize) -> Result<T::Model, Error<T::Error>> {
    item.try_bridge().map_err(|error| Error::new(error, index))
}

impl<T: TryBridge> TryBridge for Vec<T> {
    type Model = Vec<T::Model>;
    type Error = Error<T::Error>;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        self.into_iter()
            .enumerate()
            .map(|(index, item)| try_bridge_one(item, index))
            .collect()
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bridge at index `{index}`")]
pub struct Error<E: Diagnostic + 'static> {
    #[source]
    #[diagnostic_source]
    pub source: E,
    pub index: usize,
}

impl<E: Diagnostic + 'static> Error<E> {
    pub const fn new(source: E, index: usize) -> Self {
        Self { source, index }
    }
}
