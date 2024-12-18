use std::borrow::Cow;

use bon::Builder;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::{
    cow,
    schema::client::{Client as ClientSchema, Internals as InternalsSchema, Owner as OwnerSchema},
    types::UtcDateTime,
};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Client<'c> {
    pub id: Uuid,
    pub name: Cow<'c, str>,
    pub owner: Owner<'c>,
    pub created_at: UtcDateTime,
    pub description: Option<Cow<'c, str>>,
}

pub type OwnedClient = Client<'static>;

impl Client<'_> {
    pub fn into_owned(self) -> OwnedClient {
        OwnedClient {
            id: self.id,
            name: cow::into_owned(self.name),
            owner: self.owner.into_owned(),
            created_at: self.created_at,
            description: self.description.map(cow::into_owned),
        }
    }

    pub fn from_schema(schema: ClientSchema) -> Self {
        Self {
            id: schema.id,
            name: Cow::Owned(schema.name),
            owner: Owner::from_schema(schema.owner),
            created_at: schema.created_at,
            description: schema.description.map(Cow::Owned),
        }
    }
}

impl From<ClientSchema> for Client<'_> {
    fn from(schema: ClientSchema) -> Self {
        Self::from_schema(schema)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Owner<'o> {
    pub id: Uuid,
    pub name: Cow<'o, str>,
    pub created_at: UtcDateTime,
}

pub type OwnedOwner = Owner<'static>;

impl Owner<'_> {
    pub fn into_owned(self) -> OwnedOwner {
        OwnedOwner {
            id: self.id,
            name: cow::into_owned(self.name),
            created_at: self.created_at,
        }
    }

    pub fn from_schema(schema: OwnerSchema) -> Self {
        Self {
            id: schema.id,
            name: Cow::Owned(schema.name),
            created_at: schema.created_at,
        }
    }
}

impl From<OwnerSchema> for Owner<'_> {
    fn from(schema: OwnerSchema) -> Self {
        Self::from_schema(schema)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Internals<'i> {
    pub id: Uuid,
    pub secret_hash: Cow<'i, str>,
}

pub type OwnedInternals = Internals<'static>;

impl Internals<'_> {
    pub fn into_owned(self) -> OwnedInternals {
        OwnedInternals {
            id: self.id,
            secret_hash: cow::into_owned(self.secret_hash),
        }
    }

    pub fn from_schema(schema: InternalsSchema) -> Self {
        Self {
            id: schema.id,
            secret_hash: Cow::Owned(schema.secret_hash),
        }
    }
}

impl From<InternalsSchema> for Internals<'_> {
    fn from(schema: InternalsSchema) -> Self {
        Self::from_schema(schema)
    }
}
