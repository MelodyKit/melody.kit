use gel_tokio::{Client, create_client};
use melody_schema::schema::{statistics::Statistics, user::User};
use miette::Diagnostic;
use thiserror::Error;
use uuid::Uuid;

use crate::macros::{arguments, include_query};

pub const QUERY_STATISTICS: &str = include_query!("statistics/query");

pub const QUERY_USER: &str = include_query!("users/query");
pub const QUERY_USER_BY_TAG: &str = include_query!("users/query_by_tag");

#[derive(Debug, Error, Diagnostic)]
#[error("database failed")]
#[diagnostic(code(melody::database), help("see the report for more information"))]
pub struct Error(#[from] pub gel_tokio::Error);

#[derive(Debug, Clone)]
pub struct Database {
    pub client: Client,
}

impl Database {
    pub fn new(client: Client) -> Self {
        Self { client }
    }

    pub async fn create() -> Result<Self, Error> {
        let client = create_client().await?;

        Ok(Self::new(client))
    }

    pub async fn query_statistics(&self) -> Result<Statistics, Error> {
        let arguments = arguments!();

        let statistics = self
            .client
            .query_required_single(QUERY_STATISTICS, &arguments)
            .await?;

        Ok(statistics)
    }

    pub async fn query_user<I: Into<Uuid>>(&self, user_id: I) -> Result<Option<User>, Error> {
        let arguments = arguments!(user_id => user_id.into());

        let optional_user = self.client.query_single(QUERY_USER, &arguments).await?;

        Ok(optional_user)
    }

    pub async fn query_user_by_tag<T: AsRef<str>>(&self, tag: T) -> Result<Option<User>, Error> {
        let arguments = arguments!(tag => tag.as_ref());

        let optional_user = self
            .client
            .query_single(QUERY_USER_BY_TAG, &arguments)
            .await?;

        Ok(optional_user)
    }
}
