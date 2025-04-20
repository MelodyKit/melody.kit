use crate::bridge::{Bridge, TryBridge};

impl<T: Bridge> Bridge for Option<T> {
    type Model = Option<T::Model>;

    fn bridge(self) -> Self::Model {
        self.map(Bridge::bridge)
    }
}

impl<T: TryBridge> TryBridge for Option<T> {
    type Model = Option<T::Model>;
    type Error = T::Error;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        self.map(TryBridge::try_bridge).transpose()
    }
}
