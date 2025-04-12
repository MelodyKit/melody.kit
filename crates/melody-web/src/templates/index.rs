use std::borrow::Cow;

use maud::{Markup, html};
use melody_model::models::statistics::Statistics;

use crate::{
    date::{Datelike, created, today},
    templates::base::{HeadContext, base, head},
};

pub const TITLE: &str = "Home";
pub const DESCRIPTION: &str = "All your music, in one place.";
pub const NO_STATISTICS: &str = "Statistics are currently unavailable.";

pub fn content(optional_statistics: Option<Statistics>) -> Markup {
    let statistics_display = match optional_statistics {
        Some(statistics) => html! {
            ul class="my-4 grid grid-cols-2 gap-x-4 gap-y-6" {
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Users" }
                    h2 { (statistics.user_count) }
                }
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Streams" }
                    h2 { (statistics.stream_count) }
                }
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Tracks" }
                    h2 { (statistics.track_count) }
                }
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Artists" }
                    h2 { (statistics.artist_count) }
                }
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Albums" }
                    h2 { (statistics.album_count) }
                }
                li {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "Playlists" }
                    h2 { (statistics.playlist_count) }
                }
            }
        },
        None => html! {
            p class="text-lg my-4" {
                (NO_STATISTICS)
            }
        },
    };

    html! {
        nav class="absolute flex w-full" {
            div class="mx-auto max-w-md sm:max-w-3xl lg:max-w-7xl px-4 sm:px-6 lg:px-8 flex w-full items-center py-4" {
                a href="/" class="mr-auto flex items-center gap-4 lg:mr-12" {
                    object
                        type="image/svg+xml" data="/static/images/gradient.svg"
                        class="w-auto h-10 pointer-events-none" title="Logo" {}
                    h3 class="text-xl" { "MelodyKit" }
                }

                div class="hidden lg:flex lg:gap-x-12" {
                    a href="/download" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Download" }
                    a href="/support" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Support" }
                    a href="/premium" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Premium" }
                }

                form class="relative ml-auto hidden md:block md:mr-10" action="/search" {
                    input class="
                        text-lg
                        h-10
                        rounded-xl
                        px-4
                        border-2
                        border-transparent
                        bg-neutral-300/50 dark:bg-black/50
                        placeholder-neutral-600 dark:placeholder-neutral-400
                        focus:border-melody-blue/75 dark:focus:border-melody-purple/75
                        focus:outline-none
                    " type="search" name="query" placeholder="Search";

                    button class="
                        absolute
                        right-0 top-0
                        mr-4 mt-2
                        text-neutral-600 dark:text-neutral-400
                    " aria-label="Search" type="submit" {
                        span class="fa-solid fa-search text-lg" {}
                    }
                }

                a href="/open" class="
                    bg-gradient-to-b
                    from-melody-purple to-melody-blue
                    inline-flex
                    items-center justify-center
                    whitespace-nowrap
                    rounded-xl
                    px-4 py-2
                    text-xl
                    my-2
                " {
                    "Open"
                }
            }
        }

        div class="
            mx-auto
            max-w-md sm:max-w-3xl lg:max-w-7xl
            px-4 sm:px-6 lg:px-8
            flex flex-col lg:flex-row
            justify-between
            gap-5 pt-20
        " {
            div class="my-12 lg:my-24 w-full lg:w-1/2" {
                h1 class="text-5xl leading-none" {
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "All" }
                    " " span class="hover:text-melody-blue dark:hover:text-melody-purple" { "your" }
                    " " span class="hover:text-melody-blue dark:hover:text-melody-purple" { "music" }
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "," }
                    br;
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "in" }
                    " " span class="hover:text-melody-blue dark:hover:text-melody-purple" { "one" }
                    " " span class="hover:text-melody-blue dark:hover:text-melody-purple" { "place" }
                    span class="hover:text-melody-blue dark:hover:text-melody-purple" { "." }
                }

                p class="text-xl text-neutral-600 dark:text-neutral-400 my-4" {
                    "Synchronize and listen to your favorite tracks across all music platforms."
                }

                a href="/intro" class="
                    flex flex-row
                    items-center gap-2
                    hover:text-melody-blue dark:hover:text-melody-purple
                    text-lg leading-none
                " {
                    "Watch the video" span class="fa-solid fa-arrow-right" {}
                }

                (statistics_display)
            }
        }

        footer class="mx-auto max-w-md sm:max-w-3xl lg:max-w-7xl px-4 sm:px-6 lg:px-8 py-16" {
            div class="grid grid-cols-2 gap-y-4 lg:flex lg:flex-row lg:justify-between mb-8" {
                div class="ml-4 flex flex-col lg:ml-0" {search
                    h4 class="mb-2 text-neutral-600 dark:text-neutral-400" { "MelodyKit" }
                    ul class="grid gap-2" {
                        li {
                            a href="/" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Home" }
                        }
                        li {
                            a href="/status" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Status" }
                        }
                    }
                }
                div class="ml-4 flex flex-col lg:ml-0" {
                    h4 class="mb-2 text-neutral-600 dark:text-neutral-400" { "Resources" }
                    ul class="grid gap-2" {
                        li {
                            a href="/download" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Download" }
                        }
                        li {
                            a href="/support" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Support" }
                        }
                        li {
                            a href="/premium" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Premium" }
                        }
                        li {
                            a href="/dev" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Developers" }
                        }
                    }
                }
                div class="ml-4 flex flex-col lg:ml-0" {
                    h4 class="mb-2 text-neutral-600 dark:text-neutral-400" { "Company" }
                    ul class="grid gap-2" {
                        li {
                            a href="/about" class="hover:text-melody-blue dark:hover:text-melody-purple" { "About" }
                        }
                        li {
                            a href="/contact" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Contact" }
                        }
                    }
                }
                div class="ml-4 flex flex-col lg:ml-0" {
                    h4 class="mb-2 text-neutral-600 dark:text-neutral-400" { "Legal" }
                    ul class="grid gap-2" {
                        li {
                            a href="/privacy" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Privacy" }
                        }
                        li {
                            a href="/terms" class="hover:text-melody-blue dark:hover:text-melody-purple" { "Terms" }
                        }
                    }
                }
            }

            div class="flex flex-row items-center justify-center" {
                a href="/discord" class="mx-4 flex flex-col lg:ml-0" aria-label="Discord" {
                    span class="fa-brands fa-discord text-discord text-3xl" {}
                }
                a href="/bluesky" class="mx-4 flex flex-col lg:ml-0" aria-label="Bluesky" {
                    span class="fa-brands fa-bluesky text-bluesky text-3xl" {}
                }
                a href="/reddit" class="mx-4 flex flex-col lg:ml-0" aria-label="Reddit" {
                    span class="fa-brands fa-reddit-alien text-reddit text-3xl" {}
                }
                a href="/youtube" class="mx-4 flex flex-col lg:ml-0" aria-label="YouTube" {
                    span class="fa-brands fa-youtube text-youtube text-3xl" {}
                }
                a href="/github" class="mx-4 flex flex-col lg:ml-0" aria-label="GitHub" {
                    span class="fa-brands fa-github text-3xl" {}
                }
            }

            p class="min-w-full text-neutral-600 dark:text-neutral-400 text-center mt-8" {
                span class="fa-regular fa-copyright hover:text-melody-blue dark:hover:text-melody-purple mr-2" {}
                "MelodyKit " (created().year()) "-" (today().year()) "." " All rights reserved."
                span class="fa-solid fa-heart hover:text-melody-blue dark:hover:text-melody-purple ml-2" {}
            }
        }
    }
}

pub fn index(optional_statistics: Option<Statistics>) -> Markup {
    base(
        &head(&HeadContext::new(
            Cow::Borrowed(TITLE),
            Cow::Borrowed(DESCRIPTION),
        )),
        &content(optional_statistics),
    )
}
