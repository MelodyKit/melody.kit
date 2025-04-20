use miette::Diagnostic;

pub trait Bridge {
    type Model;

    fn bridge(self) -> Self::Model;
}

pub trait TryBridge {
    type Model;
    type Error: Diagnostic + 'static;

    fn try_bridge(self) -> Result<Self::Model, Self::Error>;
}
