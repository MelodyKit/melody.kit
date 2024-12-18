use melody_kit::state::State;
use poise::ApplicationContext;

use crate::client::Error;

pub type Context<'c> = ApplicationContext<'c, State, Error>;
