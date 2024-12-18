use bon::Builder;
use edgedb_tokio::Queryable;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::types::UtcDateTime;

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Client {
    pub id: Uuid,
    pub name: String,
    pub owner: Owner,
    pub created_at: UtcDateTime,
    pub description: Option<String>,
}

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Owner {
    pub id: Uuid,
    pub name: String,
    pub created_at: UtcDateTime,
}

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Internals {
    pub id: Uuid,
    pub secret_hash: String,
}
