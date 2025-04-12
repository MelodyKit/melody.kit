use std::fmt::Display;

use melody_config::config::context::Context;

pub fn artist<I: Display>(context: &Context<'_>, id: I) -> String {
    format!(
        "https://{open}.{domain}/artists/{id}",
        open = context.open,
        domain = context.domain
    )
}

pub fn album<I: Display>(context: &Context<'_>, id: I) -> String {
    format!(
        "https://{open}.{domain}/albums/{id}",
        open = context.open,
        domain = context.domain
    )
}

pub fn track<I: Display>(context: &Context<'_>, id: I) -> String {
    format!(
        "https://{open}.{domain}/tracks/{id}",
        open = context.open,
        domain = context.domain
    )
}

pub fn playlist<I: Display>(context: &Context<'_>, id: I) -> String {
    format!(
        "https://{open}.{domain}/playlists/{id}",
        open = context.open,
        domain = context.domain
    )
}

pub fn user<I: Display>(context: &Context<'_>, id: I) -> String {
    format!(
        "https://{open}.{domain}/users/{id}",
        open = context.open,
        domain = context.domain
    )
}
