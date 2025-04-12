use std::sync::Arc;

use melody_state::state::{StatelessRouter, StaticState};
use miette::Diagnostic;
use thiserror::Error;
use tokio::net::TcpListener;

use crate::routes::router;

pub type Port = u16;

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bind to `{host}:{port}`")]
#[diagnostic(
    code(melody::kit::bind),
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
#[diagnostic(code(melody::kit::serve), help("see the report for more information"))]
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
#[diagnostic(
    code(melody::web::app::run),
    help("see the report for more information")
)]
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
}

pub async fn bind<H: AsRef<str> + Send>(host: H, port: Port) -> Result<TcpListener, BindError> {
    let host = host.as_ref();

    TcpListener::bind((host, port))
        .await
        .map_err(|error| BindError::new(error, host.to_owned(), port))
}

pub fn create(state: StaticState) -> StatelessRouter {
    let shared_state = Arc::new(state);

    let app = router().with_state(shared_state);

    app
}

pub async fn serve(listener: TcpListener, app: StatelessRouter) -> Result<(), ServeError> {
    axum::serve(listener, app).await.map_err(ServeError)
}

pub async fn run<H: AsRef<str> + Send>(
    host: H,
    port: Port,
    state: StaticState,
) -> Result<(), Error> {
    let app = create(state);

    let listener = bind(host, port).await.map_err(Error::bind)?;

    serve(listener, app).await.map_err(Error::serve)
}
