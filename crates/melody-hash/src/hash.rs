use argon2::{Algorithm, Argon2, Params, Version};
use bon::Builder;
use melody_config::config::hash::Hash;
use miette::Diagnostic;
use password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString};
use rand::{RngCore, rng};
use thiserror::Error;

#[derive(Debug, Error, Diagnostic)]
#[error("hasher error")]
#[diagnostic(
    code(melody::hash::hasher),
    help("make sure the hash configuration is correct")
)]
pub struct HasherError(#[from] pub argon2::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("hash error")]
#[diagnostic(code(melody::hash), help("see the report for more information"))]
pub struct Error(#[from] pub password_hash::Error);

pub type Context = Argon2<'static>;

#[derive(Debug, Clone, Builder)]
pub struct Hasher {
    pub context: Context,
    pub salt_size: usize,
}

impl Hasher {
    pub fn create(config: &Hash) -> Result<Self, HasherError> {
        let Hash {
            memory_cost,
            time_cost,
            parallelism,
            size,
            salt_size,
        } = *config;

        let algorithm = Algorithm::default();
        let version = Version::default();

        let parameters = Params::new(memory_cost, time_cost, parallelism, Some(size))?;

        let context = Context::new(algorithm, version, parameters);

        let hasher = Self::builder()
            .context(context)
            .salt_size(salt_size)
            .build();

        Ok(hasher)
    }
}

impl Hasher {
    pub fn generate_salt(&self) -> Result<SaltString, Error> {
        let mut bytes = vec![0; self.salt_size];

        rng().fill_bytes(&mut bytes);

        let string = SaltString::encode_b64(&bytes)?;

        Ok(string)
    }

    pub fn hash<P: AsRef<str>>(&self, password: P) -> Result<String, Error> {
        let salt = self.generate_salt()?;

        let password_hash = self
            .context
            .hash_password(password.as_ref().as_bytes(), salt.as_salt())?;

        let string = password_hash.to_string();

        Ok(string)
    }

    pub fn verify<P: AsRef<str>, H: AsRef<str>>(
        &self,
        password: P,
        hash: H,
    ) -> Result<Option<String>, Error> {
        let password_hash = PasswordHash::new(hash.as_ref())?;

        self.context
            .verify_password(password.as_ref().as_bytes(), &password_hash)?;

        let parameters: Params = (&password_hash).try_into()?;

        if self.context.params() == &parameters {
            Ok(None)
        } else {
            let rehash = self.hash(password)?;

            Ok(Some(rehash))
        }
    }
}
