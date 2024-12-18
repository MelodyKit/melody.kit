use poise::{macros::command, CreateReply};

use crate::{client::Error, core::Context, embeds::internal_error};

#[command(slash_command)]
pub async fn statistics(context: Context<'_>) -> Result<(), Error> {
    let state = context.data();

    let reply = if let Ok(statistics) = state.database.query_statistics().await {
        CreateReply::default()
    } else {
        CreateReply::default().embed(internal_error())
    };

    Ok(())
}
