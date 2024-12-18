use edgedb_tokio::{create_client, Client};
use miette::Diagnostic;
use thiserror::Error;
use uuid::Uuid;

use crate::models::client::OwnedInternals;
use crate::models::user::OwnedUser;
use crate::models::Statistics;

pub const QUERY_USER: &str = include_str!("queries/users/query.edgeql");
pub const QUERY_USER_BY_TAG: &str = include_str!("queries/users/query_by_tag.edgeql");

pub const QUERY_CLIENT_INTERNALS: &str = include_str!("queries/clients/internals/query.edgeql");

pub const QUERY_STATISTICS: &str = include_str!("queries/statistics/query.edgeql");

macro_rules! arguments {
    ($($name: ident => $value: expr),* $(,)?) => {
        ::std::collections::HashMap::from([
            $(
                (stringify!($name), $value),
            )*
        ])
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("database failed")]
#[diagnostic(
    code(melody_kit::database),
    help("see the report for more information")
)]
pub struct Error(#[from] pub edgedb_tokio::Error);

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

    pub async fn query_user(&self, user_id: Uuid) -> Result<Option<OwnedUser>, Error> {
        let arguments = arguments!(user_id => user_id.into());

        let user = self
            .client
            .query_single(QUERY_USER, &arguments)
            .await?
            .map(OwnedUser::from_schema);

        Ok(user)
    }

    pub async fn query_user_by_tag<S: AsRef<str>>(
        &self,
        tag: S,
    ) -> Result<Option<OwnedUser>, Error> {
        let arguments = arguments!(tag => tag.as_ref().into());

        let user = self
            .client
            .query_single(QUERY_USER_BY_TAG, &arguments)
            .await?
            .map(OwnedUser::from_schema);

        Ok(user)
    }

    pub async fn query_client_internals(
        &self,
        client_id: Uuid,
    ) -> Result<Option<OwnedInternals>, Error> {
        let arguments = arguments!(client_id => client_id.into());

        let client = self
            .client
            .query_single(QUERY_CLIENT_INTERNALS, &arguments)
            .await?
            .map(OwnedInternals::from_schema);

        Ok(client)
    }

    pub async fn query_statistics(&self) -> Result<Statistics, Error> {
        let arguments = arguments!();

        let schema = self
            .client
            .query_required_single(QUERY_STATISTICS, &arguments)
            .await?;

        let statistics = Statistics::from_schema(schema);

        Ok(statistics)
    }
}
