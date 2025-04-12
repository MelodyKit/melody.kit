use melody_state::state::StaticState;
use poise::{FrameworkOptions, builtins::register_globally};

use crate::{client::Error, commands::statistics};

pub type Framework = poise::Framework<StaticState, Error>;

pub fn build(state: StaticState) -> Framework {
    let options = FrameworkOptions {
        commands: vec![statistics()],
        ..Default::default()
    };

    Framework::builder()
        .options(options)
        .setup(|context, _ready, framework| {
            Box::pin(async move {
                register_globally(context, &framework.options().commands)
                    .await
                    .map_err(Error)?;

                Ok(state)
            })
        })
        .build()
}
