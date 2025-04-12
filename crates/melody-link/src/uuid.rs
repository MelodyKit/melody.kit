use miette::Diagnostic;
use thiserror::Error;
use uuid::Uuid;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid UUID")]
#[diagnostic(code(melody::link::uuid), help("see the report for more information"))]
pub struct Error(#[from] pub uuid::Error);

pub fn parse<S: AsRef<str>>(string: S) -> Result<Uuid, Error> {
    string.as_ref().parse().map_err(Error)
}
