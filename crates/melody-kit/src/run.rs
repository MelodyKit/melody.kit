use axum::serve;
use miette::Diagnostic;
use thiserror::Error;
use tokio::net::TcpListener;

use crate::{routes::router, state::State, types::Port};

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bind to `{host}:{port}`")]
#[diagnostic(
    code(melody_kit::run::bind),
    help("make sure the address is valid and accessible")
)]
pub struct BindError {
    pub source: std::io::Error,
    pub host: String,
    pub port: Port,
}

impl BindError {
    pub fn new(source: std::io::Error, host: String, port: Port) -> Self {
        Self { source, host, port }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("serve failed")]
#[diagnostic(
    code(melody_kit::run::serve),
    help("see the report for more information")
)]
pub struct ServeError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Bind(#[from] BindError),
    Serve(#[from] ServeError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to run")]
#[diagnostic(code(melody_kit::run), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn bind(error: BindError) -> Self {
        Self::new(error.into())
    }

    pub fn serve(error: ServeError) -> Self {
        Self::new(error.into())
    }

    pub fn new_bind(error: std::io::Error, host: String, port: Port) -> Self {
        Self::bind(BindError::new(error, host, port))
    }

    pub fn new_serve(error: std::io::Error) -> Self {
        Self::serve(ServeError(error))
    }
}

pub async fn run<H: AsRef<str>>(host: H, port: Port, state: State) -> Result<(), Error> {
    let host = host.as_ref();

    let listener = TcpListener::bind((host, port))
        .await
        .map_err(|error| Error::new_bind(error, host.to_owned(), port))?;

    let router_with_state = router().with_state(state);

    serve(listener, router_with_state)
        .await
        .map_err(Error::new_serve)?;

    Ok(())
}
