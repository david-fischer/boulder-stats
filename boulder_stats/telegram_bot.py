"""Telegram Bot."""

import json
import logging

import pandas as pd
from telegram.ext import CommandHandler, Updater

from boulder_stats.data_analysis import Analyzer
from boulder_stats.utils import next_weekday

with open("../secrets.json") as file:
    TOKEN = json.load(file)["token"]

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update, context):
    """Send start-message."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def plot(update, context):
    """Send plot as .png in current chat.

    Triggered with /command *args. Posts one plot for each arg.
    """
    analyzer = Analyzer()
    week_days = {"mo": 0, "di": 1, "mi": 2, "do": 3, "fr": 4, "sa": 5, "so": 6}
    arg_to_date = {"heute": pd.Timestamp.now().date()}
    arg_to_date["morgen"] = arg_to_date["heute"] + pd.Timedelta("1D")
    for key, val in week_days.items():
        arg_to_date[key] = next_weekday(arg_to_date["heute"], val)
    args = [arg_to_date[arg] for arg in context.args if arg in arg_to_date]
    args = args or [arg_to_date["heute"]]
    for arg in args:
        plot_fig = analyzer.get_plot_bytes(arg)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=plot_fig)


plot_handler = CommandHandler("plot", plot)
dispatcher.add_handler(plot_handler)

updater.start_polling()
