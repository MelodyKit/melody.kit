use bon::Builder;
use serde::{Deserialize, Serialize};

use crate::{impl_default_with_builder, types::Cost};

pub const DEFAULT_MEMORY_COST: Cost = 65536;
pub const DEFAULT_TIME_COST: Cost = 4;
pub const DEFAULT_PARALLELISM: Cost = 4;
pub const DEFAULT_SIZE: usize = 32;
pub const DEFAULT_SALT_SIZE: usize = 16;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Hash {
    #[builder(default = DEFAULT_MEMORY_COST)]
    pub memory_cost: Cost,

    #[builder(default = DEFAULT_TIME_COST)]
    pub time_cost: Cost,

    #[builder(default = DEFAULT_PARALLELISM)]
    pub parallelism: Cost,

    #[builder(default = DEFAULT_SIZE)]
    pub size: usize,

    #[builder(default = DEFAULT_SALT_SIZE)]
    pub salt_size: usize,
}

impl_default_with_builder!(Hash);
