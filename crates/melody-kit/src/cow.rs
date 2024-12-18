use std::borrow::Cow;

pub fn into_owned<T: ?Sized + ToOwned>(input: Cow<'_, T>) -> Cow<'static, T> {
    Cow::Owned(input.into_owned())
}
