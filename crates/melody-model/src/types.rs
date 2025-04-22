use non_empty_str::CowStr;

pub type Count = u64;

pub type Genres<'g> = Vec<CowStr<'g>>;
pub type StaticGenres = Genres<'static>;
