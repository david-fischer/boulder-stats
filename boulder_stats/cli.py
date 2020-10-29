"""This script provides the main function which serves as entry-point for setup.py."""
import logging

import click
import matplotlib
from apscheduler.schedulers.blocking import BlockingScheduler
from xvfbwrapper import Xvfb

from .data_analysis import Analyzer
from .data_collector import DataCollector
from .telegram_bot import Bot

matplotlib.use("Agg")
vdisplay = Xvfb()
vdisplay.start()

pass_bot = click.make_pass_decorator(Bot, ensure=True)
pass_dc = click.make_pass_decorator(DataCollector, ensure=True)
pass_da = click.make_pass_decorator(Analyzer, ensure=True)
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


@data.command()
@pass_dc
def schedule(data_collector):
    """Use scheduler to periodically collect data for the next 7 days."""
    scheduler = BlockingScheduler()
    scheduler.add_job(data_collector.collect, trigger="cron", minute="15,45")
    scheduler.start()


@data.command()
@pass_dc
def collect(data_collector):
    """Collect data for the next 7 days."""
    data_collector.collect()


# @data.command()
# @pass_da
# def show(analyzer, date=pd.Timestamp.today()):
#     df = analyzer.get_currently_booked_day(date)
#     calc_cummulated_visitors(df)
#     nice_plot(df)
#     plt.show()


if __name__ == "__main__":
    cli()
