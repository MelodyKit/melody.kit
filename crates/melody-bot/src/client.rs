use melody_state::state::StaticState;
use miette::Diagnostic;
use serenity::{Client, all::GatewayIntents};
use thiserror::Error;

use crate::framework;

#[derive(Debug, Error, Diagnostic)]
#[error("client error")]
#[diagnostic(
    code(melody::discord::client),
    help("see the report for more information")
)]
pub struct Error(#[from] pub serenity::Error);

pub async fn build<T: AsRef<str>>(token: T, state: StaticState) -> Result<Client, Error> {
    let intents = GatewayIntents::non_privileged();

    Client::builder(token, intents)
        .framework(framework::build(state))
        .await
        .map_err(Error)
}

pub async fn start(mut client: Client) -> Result<(), Error> {
    client.start().await.map_err(Error)
}

pub async fn run<T: AsRef<str>>(token: T, state: StaticState) -> Result<(), Error> {
    let client = build(token, state).await?;

    start(client).await?;

    Ok(())
}
