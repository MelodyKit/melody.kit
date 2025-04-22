use melody_model::types::StaticGenres;
use melody_schema::types::Genres as GenresSchema;
use miette::Diagnostic;
use non_empty_str::Empty;
use thiserror::Error;

use crate::{bridge::TryBridge, vec};

#[derive(Debug, Error, Diagnostic)]
#[error("empty genre encountered")]
#[diagnostic(
    code(melody::bridge::genre::empty),
    help("make sure all genres are non-empty")
)]
pub struct Error(#[from] pub vec::Error<Empty>);

pub fn try_bridge(schema: GenresSchema) -> Result<StaticGenres, Error> {
    let model = schema.try_bridge()?;

    Ok(model)
}
