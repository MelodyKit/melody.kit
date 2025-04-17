use melody_link::{
    id::Id,
    tag::{self, StaticTag, Tag},
};
use melody_schema::types::{Count as CountSchema, Id as IdSchema};
use non_empty_str::{CowStr, Empty, StaticCowStr};

pub type Count = u64;

pub const fn count_from_schema(schema: CountSchema) -> Count {
    schema.unsigned_abs()
}

pub const fn id_from_schema(schema: IdSchema) -> Id {
    Id::new(schema)
}

pub const fn borrowed_from_schema(schema: &str) -> Result<CowStr<'_>, Empty> {
    CowStr::borrowed(schema)
}

pub fn owned_from_schema(schema: String) -> Result<StaticCowStr, Empty> {
    CowStr::owned(schema)
}

pub fn tag_from_schema(schema: String) -> Result<StaticTag, tag::Error> {
    Tag::owned(schema)
}
