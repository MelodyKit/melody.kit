use std::path::PathBuf;

use clap::{Args, Parser, Subcommand};
use melody_bot::composed::composed as composed_bot;
use melody_kit::{
    build::build, composed::composed as composed_kit, config::core::OwnedConfig, init::init,
    keyring::OwnedKeyring, prepare::prepare, types::Port,
};
use miette::Diagnostic;
use thiserror::Error;
use tokio::runtime::Runtime;

#[derive(Debug, Args)]
pub struct Globals {
    /// The directory to change to before doing anything.
    #[arg(
        short = 'D',
        long,
        global = true,
        name = "DIRECTORY",
        help = "Change to this directory before doing anything"
    )]
    pub directory: Option<PathBuf>,

    /// The path to the config file to use.
    #[arg(
        short = 'C',
        long,
        global = true,
        name = "FILE",
        help = "Use the config from this file"
    )]
    pub config: Option<PathBuf>,
}

#[derive(Debug, Parser)]
#[command(
    author,
    version,
    about,
    propagate_version = true,
    arg_required_else_help = true
)]
pub struct App {
    /// The global options to use.
    #[command(flatten)]
    pub globals: Globals,
    /// The subcommand to run, if any.
    #[command(subcommand)]
    pub command: Command,
}

pub type KitError = melody_kit::composed::Error;
pub type BotError = melody_bot::composed::Error;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Prepare(#[from] melody_kit::prepare::Error),
    Init(#[from] melody_kit::init::Error),
    Build(#[from] melody_kit::build::Error),
    Kit(#[from] KitError),
    Bot(#[from] BotError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("error encountered")]
#[diagnostic(
    code(melody_cli::app::run),
    help("see the report for more information")
)]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn prepare(error: melody_kit::prepare::Error) -> Self {
        Self::new(error.into())
    }

    pub fn init(error: melody_kit::init::Error) -> Self {
        Self::new(error.into())
    }

    pub fn build(error: melody_kit::build::Error) -> Self {
        Self::new(error.into())
    }

    pub fn kit(error: KitError) -> Self {
        Self::new(error.into())
    }

    pub fn bot(error: BotError) -> Self {
        Self::new(error.into())
    }
}

impl App {
    pub fn run(self) -> Result<(), Error> {
        let globals = self.globals;

        prepare(globals.directory).map_err(Error::prepare)?;

        let (config, keyring) = init(globals.config).map_err(Error::init)?;

        let runtime = build().map_err(Error::build)?;

        match self.command {
            Command::Kit(kit) => kit.run(runtime, config, keyring).map_err(Error::kit)?,
            Command::Bot(bot) => bot.run(runtime, config, keyring).map_err(Error::bot)?,
        };

        Ok(())
    }
}

#[derive(Debug, Subcommand)]
pub enum Command {
    #[command(about = "Run MelodyKit API")]
    Kit(KitCommand),
    #[command(about = "Run MelodyKit bot")]
    Bot(BotCommand),
}

#[derive(Debug, Args)]
pub struct KitCommand {
    /// The host to run on.
    #[arg(short = 'H', long, name = "HOST", help = "Run on this host")]
    pub host: Option<String>,

    /// The port to run on.
    #[arg(short = 'p', long, name = "PORT", help = "Run on this port")]
    pub port: Option<Port>,
}

impl KitCommand {
    pub fn run(
        self,
        runtime: Runtime,
        config: OwnedConfig,
        keyring: OwnedKeyring,
    ) -> Result<(), KitError> {
        let host = self
            .host
            .unwrap_or_else(|| config.kit.host.as_ref().to_owned());
        let port = self.port.unwrap_or(config.kit.port);

        runtime.block_on(composed_kit(host, port, config, keyring))
    }
}

#[derive(Debug, Args)]
pub struct BotCommand {
    #[arg(short = 't', long, name = "TOKEN", help = "Use this bot token")]
    pub token: Option<String>,
}

impl BotCommand {
    pub fn run(
        self,
        runtime: Runtime,
        config: OwnedConfig,
        keyring: OwnedKeyring,
    ) -> Result<(), BotError> {
        let token = self
            .token
            .unwrap_or_else(|| keyring.bot.as_ref().to_owned());

        runtime.block_on(composed_bot(token, config, keyring))
    }
}
