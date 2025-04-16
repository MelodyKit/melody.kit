pub trait Split {
    type Common;
    type Specific;

    fn split(self) -> (Self::Common, Self::Specific);
}
