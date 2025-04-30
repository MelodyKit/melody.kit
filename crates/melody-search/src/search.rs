use std::fmt::Display;

use meilisearch_sdk::{client::Client, errors};
use miette::Diagnostic;
use thiserror::Error;

pub type Port = u16;

#[derive(Debug, Error, Diagnostic)]
#[error("search error")]
#[diagnostic(code(melody::search), help("see the report for more information"))]
pub struct Error(#[from] pub errors::Error);

#[derive(Debug, Clone)]
pub struct Search {
    pub client: Client,
}

pub const SCHEME: &str = "http";

pub fn url<H: Display>(host: H, port: Port) -> String {
    format!("{SCHEME}://{host}:{port}")
}

impl Search {
    pub fn new(client: Client) -> Self {
        Self { client }
    }

    pub fn create<H: AsRef<str>, K: AsRef<str>>(
        host: H,
        port: Port,
        key: K,
    ) -> Result<Self, Error> {
        let client = Client::new(url(host.as_ref(), port), Some(key.as_ref()))?;

        let search = Self::new(client);

        Ok(search)
    }
}
