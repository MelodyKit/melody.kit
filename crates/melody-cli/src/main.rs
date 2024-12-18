use clap::Parser;
use melody_cli::app::App;
use miette::Result;

fn main() -> Result<()> {
    App::parse().run()?;

    Ok(())
}
