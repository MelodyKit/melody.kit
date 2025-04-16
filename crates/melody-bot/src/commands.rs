use melody_model::models::statistics::Statistics;
use poise::{CreateReply, macros::command};

use crate::{
    client::Error,
    core::Context,
    embeds::{error_embed, statistics_embed},
};

pub const INLINE: bool = false;

#[command(slash_command)]
pub async fn statistics(context: Context<'_>) -> Result<(), Error> {
    let state = context.data();

    let embed = state
        .database
        .query_statistics()
        .await
        .map(Statistics::from_schema)
        .map_or_else(error_embed, |statistics| statistics_embed(&statistics));

    let reply = CreateReply::default().embed(embed);

    context.send(reply).await?;

    Ok(())
}
