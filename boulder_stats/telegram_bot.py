"""Telegram Bot."""

import json
import logging
from secrets import compare_digest

import pandas as pd
from telegram.ext import CommandHandler, Updater

from boulder_stats.data_analysis import Analyzer
from boulder_stats.utils import next_weekday

with open("../secrets.json") as file:
    SECRETS = json.load(file)
    print(SECRETS)


def save_secrets():
    """Save current ``SECRETS```as .json-file."""
    print(SECRETS)
    with open("../secrets.json", "w") as file:  # pylint: disable=redefined-outer-name
        json.dump(SECRETS, file, indent=4)


updater = Updater(token=SECRETS["token"], use_context=True)
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


def unlock(update, context):
    """Unlock bot if user provides correct password as first arg."""
    if str(update.effective_chat.id) in SECRETS["chat_ids"]:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Bot is already unlocked."
        )
        return
    args = context.args
    password = args[0] if len(args) == 1 else None
    if compare_digest(password, SECRETS["unlock_pw"]):
        chat = update.effective_chat
        chat_name = chat.title or chat.first_name + " " + chat.last_name
        SECRETS["chat_ids"][str(chat.id)] = chat_name
        save_secrets()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot unlocked.")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Wrong password."
        )


plot_handler = CommandHandler("plot", plot)
dispatcher.add_handler(plot_handler)
unlock_handler = CommandHandler("unlock", unlock)
dispatcher.add_handler(unlock_handler)

updater.start_polling()
