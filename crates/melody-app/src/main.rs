use clap::Parser;
use melody_app::app::App;
use miette::Result;

fn main() -> Result<()> {
    App::parse().execute()?;

    Ok(())
}
