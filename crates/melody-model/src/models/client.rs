use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Client<'c> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub name: CowStr<'c>,
    #[builder(into)]
    pub owner: Owner<'c>,
    #[builder(into)]
    pub created_at: UtcDateTime,
    #[builder(into)]
    pub description: Option<CowStr<'c>>,
}

pub type StaticClient = Client<'static>;

impl IntoStatic for Client<'_> {
    type Static = StaticClient;

    fn into_static(self) -> Self::Static {
        Self::Static {
            id: self.id,
            name: self.name.into_static(),
            owner: self.owner.into_static(),
            created_at: self.created_at,
            description: self.description.into_static(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Owner<'o> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub name: CowStr<'o>,
    #[builder(into)]
    pub created_at: UtcDateTime,
}

pub type StaticOwner = Owner<'static>;

impl IntoStatic for Owner<'_> {
    type Static = StaticOwner;

    fn into_static(self) -> Self::Static {
        Self::Static {
            id: self.id,
            name: self.name.into_static(),
            created_at: self.created_at,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Internals<'i> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub secret_hash: CowStr<'i>,
}

pub type StaticInternals = Internals<'static>;

impl IntoStatic for Internals<'_> {
    type Static = StaticInternals;

    fn into_static(self) -> Self::Static {
        Self::Static {
            id: self.id,
            secret_hash: self.secret_hash.into_static(),
        }
    }
}
