use std::sync::Arc;

use expand_tilde::ExpandTilde;
use melody_state::state::{StatelessRouter, StaticState};
use miette::Diagnostic;
use thiserror::Error;
use tokio::net::TcpListener;
use tower_http::services::ServeDir;

use crate::routes::router;

pub type Port = u16;

pub const STATIC: &str = "/static";

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bind to `{host}:{port}`")]
#[diagnostic(
    code(melody::web::bind),
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
#[diagnostic(code(melody::web::serve), help("see the report for more information"))]
pub struct ServeError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Bind(#[from] BindError),
    Serve(#[from] ServeError),
    ExpandTilde(#[from] expand_tilde::Error),
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

    pub fn expand_tilde(error: expand_tilde::Error) -> Self {
        Self::new(error.into())
    }
}

pub async fn bind<H: AsRef<str> + Send>(host: H, port: Port) -> Result<TcpListener, BindError> {
    let host = host.as_ref();

    TcpListener::bind((host, port))
        .await
        .map_err(|error| BindError::new(error, host.to_owned(), port))
}

pub fn create(state: StaticState) -> Result<StatelessRouter, expand_tilde::Error> {
    let path = state.config.web.path.get().expand_tilde_owned()?;

    let service = ServeDir::new(path);

    let shared_state = Arc::new(state);

    let app = router()
        .with_state(shared_state)
        .nest_service(STATIC, service);

    Ok(app)
}

pub async fn serve(listener: TcpListener, app: StatelessRouter) -> Result<(), ServeError> {
    axum::serve(listener, app).await.map_err(ServeError)
}

pub async fn run<H: AsRef<str> + Send>(
    host: H,
    port: Port,
    state: StaticState,
) -> Result<(), Error> {
    let app = create(state).map_err(Error::expand_tilde)?;

    let listener = bind(host, port).await.map_err(Error::bind)?;

    serve(listener, app).await.map_err(Error::serve)
}
