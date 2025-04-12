use bon::Builder;
use into_static::IntoStatic;
use serde::{Deserialize, Serialize};

use crate::{
    config::{
        context::Context,
        email::Email,
        hash::Hash,
        image::Image,
        keyring::Keyring,
        kit::Kit,
        redis::Redis,
        secrets::{Access, Authorization, Refresh, Verification},
        totp::Totp,
        web::Web,
    },
    impl_default_with_builder, impl_from_path_with_toml,
};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Config<'c> {
    #[builder(default)]
    pub context: Context<'c>,

    #[builder(default)]
    pub keyring: Keyring<'c>,

    #[builder(default)]
    pub email: Email<'c>,

    #[builder(default)]
    pub hash: Hash,

    #[builder(default)]
    pub kit: Kit<'c>,

    #[builder(default)]
    pub image: Image<'c>,

    #[builder(default)]
    pub redis: Redis<'c>,

    #[builder(default)]
    pub totp: Totp,

    #[builder(default)]
    pub web: Web<'c>,

    #[builder(default)]
    pub verification: Verification,

    #[builder(default)]
    pub authorization: Authorization,

    #[builder(default)]
    pub access: Access,

    #[builder(default)]
    pub refresh: Refresh,
}

impl IntoStatic for Config<'_> {
    type Static = Config<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .context(self.context.into_static())
            .keyring(self.keyring.into_static())
            .email(self.email.into_static())
            .hash(self.hash)
            .kit(self.kit.into_static())
            .image(self.image.into_static())
            .redis(self.redis.into_static())
            .totp(self.totp)
            .web(self.web.into_static())
            .verification(self.verification)
            .authorization(self.authorization)
            .access(self.access)
            .refresh(self.refresh)
            .build()
    }
}

impl_from_path_with_toml!(Config<'_>);

impl_default_with_builder!(Config<'_>);
