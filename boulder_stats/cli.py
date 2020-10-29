"""This script provides the main function which serves as entry-point for setup.py."""
import logging
import click
import matplotlib
from xvfbwrapper import Xvfb
from boulder_stats.scheduler import start_data_collection
from boulder_stats.telegram_bot import Bot

matplotlib.use("Agg")
vdisplay = Xvfb(height=1024, width=1920)
vdisplay.start()

pass_bot = click.make_pass_decorator(Bot, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Collect data and control telegram bot, that can plot the data."""


@cli.group("bot")
def bot_cli():
    """Call bot functions."""


@bot_cli.command("start")
@pass_bot
def start(bot):
    """Start the bot."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    click.echo("Starting the bot...")
    bot.start()
    click.echo("Bot started.")


@bot_cli.command("setup")
@click.option("--token", "-t", prompt=True)
@click.option("--password", "-pw", prompt=True)
@pass_bot
def setup_bot(bot, token, password):
    """Set token and password of bot."""
    click.confirm(f"Confirm token={token} pw={password}", abort=True)
    bot.set_token(token)
    bot.set_password(password)
    click.echo("Changes successful.")


@cli.group("data")
def data():
    """Call data functions."""


data.command(name="collect")(start_data_collection)

if __name__ == "__main__":
    cli()
