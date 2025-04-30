use std::{fmt::Display, process::ExitStatus};

use miette::Diagnostic;
use thiserror::Error;
use tokio::process::Command;
use tracing::info;

use crate::search::Port;

#[derive(Debug, Error, Diagnostic)]
#[error("failed to invoke search")]
#[diagnostic(
    code(melody::search::invoke),
    help("see the report for more information")
)]
pub struct Error(#[from] pub std::io::Error);

pub const SEARCH: &str = "meilisearch";

pub const ADDRESS: &str = "--http-addr";

pub const KEY: &str = "--master-key";

pub fn address<H: Display>(host: H, port: Port) -> String {
    format!("{host}:{port}")
}

pub async fn invoke<H: AsRef<str>, K: AsRef<str>>(
    host: H,
    port: Port,
    key: K,
) -> Result<ExitStatus, Error> {
    let mut command = Command::new(SEARCH);

    let address = address(host.as_ref(), port);

    info!("invoking search on `{address}`");

    command.arg(ADDRESS).arg(address);

    command.arg(KEY).arg(key.as_ref());

    let status = command.status().await?;

    Ok(status)
}
