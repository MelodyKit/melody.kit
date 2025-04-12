use std::borrow::Cow;

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

impl IntoStatic for Client<'_> {
    type Static = Client<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .id(self.id)
            .name(self.name.into_static())
            .owner(self.owner.into_static())
            .created_at(self.created_at)
            .maybe_description(self.description.into_static())
            .build()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Owner<'o> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub name: Cow<'o, str>,
    #[builder(into)]
    pub created_at: UtcDateTime,
}

impl IntoStatic for Owner<'_> {
    type Static = Owner<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .id(self.id)
            .name(self.name.into_static())
            .created_at(self.created_at)
            .build()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Internals<'i> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub secret_hash: Cow<'i, str>,
}

impl IntoStatic for Internals<'_> {
    type Static = Internals<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .id(self.id)
            .secret_hash(self.secret_hash.into_static())
            .build()
    }
}
