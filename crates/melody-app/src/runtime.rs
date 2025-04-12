use miette::Diagnostic;
use thiserror::Error;
use tokio::runtime::{Builder, Runtime};

#[derive(Debug, Error, Diagnostic)]
#[error("failed to build runtime")]
#[diagnostic(
    code(melody::app::runtime),
    help("see the report for more information")
)]
pub struct Error(#[from] pub std::io::Error);

pub fn build() -> Result<Runtime, Error> {
    Builder::new_multi_thread()
        .enable_all()
        .build()
        .map_err(Error)
}
