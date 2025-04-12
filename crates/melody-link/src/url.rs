use miette::Diagnostic;
use thiserror::Error;
use url::ParseError;

pub use url::Url;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid URL")]
#[diagnostic(code(melody::link::url), help("check that the URL is valid"))]
pub struct Error(#[from] pub ParseError);

pub fn parse<S: AsRef<str>>(string: S) -> Result<Url, Error> {
    let url = Url::parse(string.as_ref())?;

    Ok(url)
}
