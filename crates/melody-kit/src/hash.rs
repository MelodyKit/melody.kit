use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, PasswordVerifier, SaltString},
    Algorithm, Argon2, Params, PasswordHash, Version,
};
use miette::Diagnostic;
use thiserror::Error;

use crate::config::core::Hash;

#[derive(Debug, Error, Diagnostic)]
#[error("create hash error")]
#[diagnostic(
    code(melody_kit::hash::create),
    help("make sure the hash configuration is correct")
)]
pub struct CreateError(#[from] pub argon2::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("password hash error")]
#[diagnostic(
    code(melody_kit::hash::password),
    help("make sure everything is correct")
)]
pub struct HashError(#[from] pub argon2::password_hash::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Create(#[from] CreateError),
    Hash(#[from] HashError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("hash error")]
#[diagnostic(code(melody_kit::hash), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn create(error: CreateError) -> Self {
        Self::new(error.into())
    }

    pub fn hash(error: HashError) -> Self {
        Self::new(error.into())
    }
}

pub fn create(config: &Hash) -> Result<Argon2, CreateError> {
    let &Hash {
        memory_cost,
        time_cost,
        parallelism,
        size,
    } = config;

    let algorithm = Algorithm::Argon2id;
    let version = Version::default();
    let params =
        Params::new(memory_cost, time_cost, parallelism, Some(size)).map_err(CreateError)?;

    Ok(Argon2::new(algorithm, version, params))
}

pub fn hash<P: AsRef<str>>(argon2: &Argon2<'_>, password: P) -> Result<String, HashError> {
    let salt = SaltString::generate(&mut OsRng);

    let hash = argon2.hash_password(password.as_ref().as_bytes(), &salt)?;

    Ok(format!("{hash}"))
}

pub fn verify<P: AsRef<str>, H: AsRef<str>>(
    argon2: &Argon2<'_>,
    password: P,
    hash: H,
) -> Result<(), HashError> {
    let password_hash = PasswordHash::new(hash.as_ref()).map_err(HashError)?;

    argon2
        .verify_password(password.as_ref().as_bytes(), &password_hash)
        .map_err(HashError)
}

pub fn create_hash<P: AsRef<str>>(config: &Hash, password: P) -> Result<String, Error> {
    let argon2 = create(config).map_err(Error::create)?;

    hash(&argon2, password).map_err(Error::hash)
}

pub fn create_verify<P: AsRef<str>, H: AsRef<str>>(
    config: &Hash,
    password: P,
    hash: H,
) -> Result<(), Error> {
    let argon2 = create(config).map_err(Error::create)?;

    verify(&argon2, password, hash).map_err(Error::hash)
}
