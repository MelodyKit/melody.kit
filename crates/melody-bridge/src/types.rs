use std::convert::Infallible;

use melody_model::types::Count;
use melody_schema::types::Count as CountSchema;

use crate::bridge::Bridge;

impl Bridge for CountSchema {
    type Model = Count;
    type Error = Infallible;

    fn bridge(self) -> Result<Self::Model, Self::Error> {
        Ok(self.unsigned_abs())
    }
}
