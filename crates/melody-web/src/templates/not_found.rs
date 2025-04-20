use maud::{Markup, html};
use non_empty_str::{StaticCowStr, const_borrowed_str};

use crate::templates::base::{HeadContext, base, head};

pub const TITLE: StaticCowStr = const_borrowed_str!("Error :(");
pub const DESCRIPTION: StaticCowStr = const_borrowed_str!("This page does not exist.");

pub fn content() -> Markup {
    html! {
        h1 {
            ("Error :(")
        }

        p {
            "This page does not exist."
        }
    }
}

pub fn not_found() -> Markup {
    let head_context = HeadContext::builder()
        .title(TITLE)
        .description(DESCRIPTION)
        .build();

    base(&head(&head_context), &content())
}
