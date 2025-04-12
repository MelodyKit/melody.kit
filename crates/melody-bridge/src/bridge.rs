pub trait Bridge: Sized {
    type Model;
    type Error;

    fn bridge(self) -> Result<Self::Model, Self::Error>;
}

impl<B: Bridge> Bridge for Option<B> {
    type Model = Option<B::Model>;
    type Error = B::Error;

    fn bridge(self) -> Result<Self::Model, Self::Error> {
        self.map(Bridge::bridge).transpose()
    }
}
