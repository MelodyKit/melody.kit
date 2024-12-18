use std::{borrow::Cow, collections::HashMap};

use bon::Builder;
use miette::Diagnostic;
use serde::{Deserialize, Serialize};
use thiserror::Error;
use url::Url;

use crate::{cow, types::Count};

#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse `{string}` into URL")]
#[diagnostic(
    code(melody_kit::models::pagination),
    help("make sure the URL is valid")
)]
pub struct Error {
    pub string: String,
}

impl Error {
    pub fn new(string: String) -> Self {
        Self { string }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Pagination<'p> {
    pub previous: Option<Cow<'p, str>>,
    pub next: Option<Cow<'p, str>>,
    pub count: Count,
}

pub type OwnedPagination = Pagination<'static>;

impl Pagination<'_> {
    pub fn into_owned(self) -> OwnedPagination {
        OwnedPagination {
            previous: self.previous.map(cow::into_owned),
            next: self.next.map(cow::into_owned),
            count: self.count,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Context {
    pub offset: Count,
    pub limit: Count,
    pub count: Count,
}

pub fn parse_url<S: AsRef<str>>(string: S) -> Result<Url, Error> {
    let string = string.as_ref();

    Url::parse(string).map_err(|_| Error::new(string.to_owned()))
}

pub const OFFSET: &str = "offset";
pub const LIMIT: &str = "limit";

impl Pagination<'_> {
    pub fn paginate<S: AsRef<str>>(string: S, context: Context) -> Result<Self, Error> {
        let string = string.as_ref();

        let mut url = parse_url(string)?;

        let Context {
            offset,
            limit,
            count,
        } = context;

        let mut query: HashMap<String, String> = url.query_pairs().into_owned().collect();

        url.set_query(None);

        query.insert(LIMIT.to_owned(), limit.to_string());

        let after = offset.saturating_add(limit);

        let next = (after < count).then(|| {
            query.insert(OFFSET.to_owned(), after.to_string());

            url.query_pairs_mut().extend_pairs(query.iter());

            let string = url.as_str().to_owned();

            url.set_query(None);

            string
        });

        let previous = (offset > 0).then(|| {
            let before = offset.saturating_sub(limit);

            query.insert(OFFSET.to_owned(), before.to_string());

            url.query_pairs_mut().extend_pairs(query.iter());

            let string = url.as_str().to_owned();

            url.set_query(None);

            string
        });

        let pagination = Self::builder()
            .maybe_previous(previous.map(Cow::Owned))
            .maybe_next(next.map(Cow::Owned))
            .count(count)
            .build();

        Ok(pagination)
    }
}
