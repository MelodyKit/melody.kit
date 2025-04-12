use std::borrow::Cow;

use maud::{DOCTYPE, Markup, html};
use serde::{Deserialize, Serialize};

pub const ICONS: &str = "https://kit.fontawesome.com/a4c3b493b0.js";

pub const IMAGE: &str = "https://melodykit.app/static/images/icon.png";

pub const IMAGE_PNG: &str = "/static/images/icon.png";
pub const IMAGE_SVG: &str = "/static/images/icon.svg";

pub const STYLE: &str = "/static/css/output.css";

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HeadContext<'c> {
    pub title: Cow<'c, str>,
    pub description: Cow<'c, str>,
}

impl<'c> HeadContext<'c> {
    pub fn new(title: Cow<'c, str>, description: Cow<'c, str>) -> Self {
        Self { title, description }
    }
}

pub fn head(context: &HeadContext<'_>) -> Markup {
    html! {
        head {
            meta charset="utf-8";

            meta name="viewport" content="width=device-width, initial-scale=1";

            meta name="description" content=(context.description);

            meta property="og:site_name" content="MelodyKit";
            meta property="og:title" content=(context.title);
            meta property="og:description" content=(context.description);
            meta property="og:image" content=(IMAGE);

            link rel="icon" type="image/svg+xml" href=(IMAGE_SVG);
            link rel="icon" type="image/png" href=(IMAGE_PNG);

            link rel="apple-touch-icon" href=(IMAGE_PNG);

            script async src=(ICONS) crossorigin="anonymous" {}

            link rel="preload" href=(STYLE) as="style";
            link rel="stylesheet" href=(STYLE);

            title { (context.title) }
        }
    }
}

pub fn wrap(body: &Markup) -> Markup {
    html! {
        body class="
            antialiased
            transition
            ease-in-out
            bg-neutral-50
            dark:bg-neutral-900
            min-h-screen
            bg-no-repeat
            bg-gradient-to-b
            from-melody-purple/15
            to-melody-blue/15
            text-neutral-900
            dark:text-neutral-50
            font-medium
        " {
            (body)
        }
    }
}

pub fn base(head: &Markup, body: &Markup) -> Markup {
    html! {
        (DOCTYPE)
        html lang="en" {
            (head)
            (wrap(body))
        }
    }
}
