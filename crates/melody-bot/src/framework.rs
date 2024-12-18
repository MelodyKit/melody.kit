use melody_kit::state::State;
use poise::{builtins::register_globally, FrameworkOptions};

use crate::{client::Error, commands::statistics};

pub type Framework = poise::Framework<State, Error>;

pub fn build(state: State) -> Framework {
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
