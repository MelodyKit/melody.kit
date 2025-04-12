use std::path::PathBuf;

use clap::{Args, Parser, Subcommand};
use clap_verbosity_flag::{InfoLevel, Verbosity};
use melody_bot::client as bot;
use melody_kit::kit;
use melody_state::state::StaticState;
use melody_web::web;
use miette::Diagnostic;
use thiserror::Error;

use crate::{init, prepare, runtime, setup};

pub type Port = u16;

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

    /// The verbosity level to use.
    #[command(flatten)]
    pub verbosity: Verbosity<InfoLevel>,

    /// The subcommand to run, if any.
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Prepare(#[from] prepare::Error),
    Init(#[from] init::Error),
    Runtime(#[from] runtime::Error),
    Setup(#[from] setup::Error),
    Bot(#[from] bot::Error),
    Kit(#[from] kit::Error),
    Web(#[from] web::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("error encountered")]
#[diagnostic(code(melody::app::app), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn prepare(error: prepare::Error) -> Self {
        Self::new(error.into())
    }

    pub fn init(error: init::Error) -> Self {
        Self::new(error.into())
    }

    pub fn runtime(error: runtime::Error) -> Self {
        Self::new(error.into())
    }

    pub fn setup(error: setup::Error) -> Self {
        Self::new(error.into())
    }

    pub fn bot(error: bot::Error) -> Self {
        Self::new(error.into())
    }

    pub fn web(error: web::Error) -> Self {
        Self::new(error.into())
    }

    pub fn kit(error: kit::Error) -> Self {
        Self::new(error.into())
    }
}

impl App {
    pub fn execute(self) -> Result<(), Error> {
        let globals = self.globals;

        prepare::prepare(globals.directory, self.verbosity).map_err(Error::prepare)?;

        let parts = init::init(globals.config).map_err(Error::init)?;

        let runtime = runtime::build().map_err(Error::runtime)?;

        runtime.block_on(async {
            let state = setup::setup(parts).await.map_err(Error::setup)?;

            match self.command {
                Command::Bot(command) => command.run(state).await.map_err(Error::bot),
                Command::Kit(command) => command.run(state).await.map_err(Error::kit),
                Command::Web(command) => command.run(state).await.map_err(Error::web),
            }
        })
    }
}

pub trait Runnable {
    type Error;

    fn run(self, state: StaticState) -> impl Future<Output = Result<(), Self::Error>>;
}

#[derive(Debug, Subcommand)]
pub enum Command {
    Bot(BotCommand),
    Kit(KitCommand),
    Web(WebCommand),
}

#[derive(Debug, Args)]
pub struct BotCommand {
    #[arg(short = 'T', long, name = "TOKEN", help = "Use this bot token")]
    pub override_token: Option<String>,
}

impl Runnable for BotCommand {
    type Error = bot::Error;

    async fn run(self, state: StaticState) -> Result<(), Self::Error> {
        let token = self
            .override_token
            .unwrap_or_else(|| state.keyring.bot.get().to_owned());

        bot::run(token, state).await
    }
}

#[derive(Debug, Args)]
pub struct KitCommand {
    /// The host to run on.
    #[arg(short = 'H', long, name = "HOST", help = "Run on this host")]
    pub override_host: Option<String>,

    /// The port to run on.
    #[arg(short = 'P', long, name = "PORT", help = "Run on this port")]
    pub override_port: Option<Port>,
}

impl Runnable for KitCommand {
    type Error = kit::Error;

    async fn run(self, state: StaticState) -> Result<(), Self::Error> {
        let host = self
            .override_host
            .unwrap_or_else(|| state.config.kit.host.get().to_owned());

        let port = self.override_port.unwrap_or(state.config.kit.port);

        kit::run(host, port, state).await
    }
}

#[derive(Debug, Args)]
pub struct WebCommand {
    /// The host to run on.
    #[arg(short = 'H', long, name = "HOST", help = "Run on this host")]
    pub override_host: Option<String>,

    /// The port to run on.
    #[arg(short = 'P', long, name = "PORT", help = "Run on this port")]
    pub override_port: Option<Port>,
}

impl Runnable for WebCommand {
    type Error = web::Error;

    async fn run(self, state: StaticState) -> Result<(), Self::Error> {
        let host = self
            .override_host
            .unwrap_or_else(|| state.config.web.host.get().to_owned());

        let port = self.override_port.unwrap_or(state.config.web.port);

        web::run(host, port, state).await
    }
}
