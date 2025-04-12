use keyring::Entry;
use miette::Diagnostic;
use non_empty_str::{Empty, OwnedStr};
use thiserror::Error;

#[derive(Debug, Error, Diagnostic)]
#[error("wrapped keyring error")]
#[diagnostic(
    code(melody::keyring::wrapped),
    help("see the report for more information")
)]
pub struct KeyringError(#[from] pub keyring::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Keyring(#[from] KeyringError),
    Empty(#[from] Empty),
}

#[derive(Debug, Error, Diagnostic)]
#[error("can not find `{name}` in `{service}`")]
#[diagnostic(
    code(melody::keyring::find),
    help("make sure the keyring is configured correctly")
)]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
    pub service: String,
    pub name: String,
}

impl Error {
    pub fn new(source: ErrorSource, service: String, name: String) -> Self {
        Self {
            source,
            service,
            name,
        }
    }

    pub fn keyring(error: KeyringError, service: String, name: String) -> Self {
        Self::new(error.into(), service, name)
    }

    pub fn empty(error: Empty, service: String, name: String) -> Self {
        Self::new(error.into(), service, name)
    }
}

pub fn find<S: AsRef<str>, T: AsRef<str>>(service: S, name: T) -> Result<OwnedStr, Error> {
    fn find_inner(service: &str, name: &str) -> Result<String, KeyringError> {
        let string = Entry::new(service, name)?.get_password()?;

        Ok(string)
    }

    let service_str = service.as_ref();
    let name_str = name.as_ref();

    let string = find_inner(service_str, name_str)
        .map_err(|error| Error::keyring(error, service_str.to_owned(), name_str.to_owned()))?;

    let loaded = OwnedStr::new(string)
        .map_err(|error| Error::empty(error, service_str.to_owned(), name_str.to_owned()))?;

    Ok(loaded)
}
