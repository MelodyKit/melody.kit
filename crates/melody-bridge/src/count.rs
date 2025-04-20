use melody_model::types::Count;
use melody_schema::types::Count as CountSchema;

use crate::bridge::Bridge;

impl Bridge for CountSchema {
    type Model = Count;

    fn bridge(self) -> Self::Model {
        self.unsigned_abs()
    }
}
