use melody_state::state::StaticState;
use poise::ApplicationContext;

use crate::client::Error;

pub type Context<'c> = ApplicationContext<'c, StaticState, Error>;
