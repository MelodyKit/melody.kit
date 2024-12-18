//! Loading values from paths.

use std::path::Path;

/// Loading values from paths.
pub trait Load: Sized {
    /// The associated error type returned from [`load`] on failure.
    ///
    /// [`load`]: Self::load
    type Error;

    /// Loads the value of this type from the given path.
    ///
    /// # Errors
    ///
    /// Returns [`Error`] when loading fails.
    ///
    /// [`Error`]: Self::Error
    fn load<P: AsRef<Path>>(path: P) -> Result<Self, Self::Error>;
}

/// Loads the value of the type given from the given path.
///
/// # Errors
///
/// Returns [`Error`] when loading fails.
///
/// [`Error`]: Load::Error
pub fn load<L: Load, P: AsRef<Path>>(path: P) -> Result<L, L::Error> {
    L::load(path)
}
