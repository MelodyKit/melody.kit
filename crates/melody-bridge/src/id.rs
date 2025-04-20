use melody_link::id::Id;
use melody_schema::types::Id as IdSchema;

use crate::bridge::Bridge;

impl Bridge for IdSchema {
    type Model = Id;

    fn bridge(self) -> Self::Model {
        Self::Model::new(self)
    }
}
