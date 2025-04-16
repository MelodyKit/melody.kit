use melody_link::id::Id;
use melody_schema::types::{Count as CountSchema, Id as IdSchema};

pub type Count = u64;

pub const fn count_from_schema(schema: CountSchema) -> Count {
    schema.unsigned_abs()
}

pub const fn id_from_schema(schema: IdSchema) -> Id {
    Id::new(schema)
}
