use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Client<'c> {
    pub id: Id,
    pub name: CowStr<'c>,
    pub owner: Owner<'c>,
    pub created_at: UtcDateTime,
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
    pub id: Id,
    pub name: CowStr<'o>,
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
