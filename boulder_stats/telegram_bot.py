"""Telegram Bot."""
# import os
# import sys
#
# if __name__ == "__main__":
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     __package__ = "boulder_stats"  # pylint: disable= redefined-builtin
#

import json
import logging
from functools import wraps
from secrets import compare_digest

import attr
import pandas as pd
from telegram.ext import CommandHandler, Updater

from .data_analysis import Analyzer
from .utils import next_weekday
from .paths import SECRET_PATH


def lock(func):
    """Only execute ``func`` if the bot has authorized this chat."""

    @wraps(func)
    def wrapper(bot, update, context):
        if bot.is_unlocked(update.effective_chat.id):
            return func(bot, update, context)
        return None

    return wrapper


@attr.s(auto_attribs=True)
class Bot:
    """Bot."""

    updater: Updater = None
    dispatcher: object = None
    secret_path: str = SECRET_PATH
    secrets: dict = None
    analyzer: Analyzer = None

    def __attrs_post_init__(self):
        self.load_secrets()
        self.analyzer = Analyzer()
        self.updater = Updater(token=self.secrets["token"], use_context=True)
        self.dispatcher = self.updater.dispatcher

    def load_secrets(self):
        """Load :attr:`secrets` from :attr:`secret_path`."""
        with open(self.secret_path) as file:
            self.secrets = json.load(file)

    def save_secrets(self):
        """Save current :attr:`secrets` as .json-file."""
        with open(self.secret_path, "w") as file:
            json.dump(self.secrets, file, indent=4)

    def start(self):
        """Start listening to commands in chats."""
        self.updater.start_polling()

    def add_chat_id(self, chat):
        """Add chat_id to list of authorized_chats."""
        chat_name = chat.title or chat.first_name + " " + chat.last_name
        self.secrets["chat_ids"][str(chat.id)] = chat_name
        self.save_secrets()

    def is_unlocked(self, chat_id):
        """Check if chat is authorized."""
        return str(chat_id) in self.secrets["chat_ids"]

    @staticmethod
    def send_text(update, context, text):
        """Send text-message to chat."""
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    @staticmethod
    def send_photo(update, context, photo):
        """Send photo to chat."""
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    @staticmethod
    def parsed_plot_args(args):
        """Return list of datestamps for args. args can be weekdays, "heute" or "morgen"."""
        week_days = {"mo": 0, "di": 1, "mi": 2, "do": 3, "fr": 4, "sa": 5, "so": 6}
        arg_to_date = {"heute": pd.Timestamp.now().date()}
        arg_to_date["morgen"] = arg_to_date["heute"] + pd.Timedelta("1D")
        for key, val in week_days.items():
            arg_to_date[key] = next_weekday(arg_to_date["heute"], val)
        parsed_args = [arg_to_date[arg] for arg in args if arg in arg_to_date]
        return parsed_args or [arg_to_date["heute"]]

    @lock
    def plot(self, update, context):
        """Send plots for parsed_args to chat."""
        args = self.parsed_plot_args(context.args)
        self.analyzer.reload()
        for arg in args:
            plot_fig = self.analyzer.get_plot_bytes(arg)
            self.send_photo(update, context, plot_fig)

    def unlock(self, update, context):
        """If bot is not unlocked and arg[0] matches :attr:`secrets`["unlock_pw"]", unlock chat."""
        chat = update.effective_chat
        if self.is_unlocked(chat.id):
            self.send_text(update, context, "Bot is already unlocked.")
            return
        password = context.args[0] if len(context.args) == 1 else ""
        if compare_digest(password, self.secrets["unlock_pw"]):
            self.add_chat_id(chat)
            self.send_text(update, context, "Bot unlocked.")
        else:
            self.send_text(update, context, "Wrong password.")

    def set_token(self, token):
        """Set bot token."""
        self.secrets["token"] = token
        self.save_secrets()

    def set_password(self, password):
        """Set unlock password."""
        self.secrets["unlock_pw"] = password

    def add_handler(self, cmd, function):
        """Add handler to listen to.

        The bot executes ``function`` with the user writes ``/cmd arg1 arg2 ...". Arguments are available via
        ``context.args``.
        """
        self.dispatcher.add_handler(CommandHandler(cmd, function))


def start_bot():
    """Start bot."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    bot = Bot()
    bot.add_handler("plot", bot.plot)
    bot.add_handler("unlock", bot.unlock)
    bot.start()


if __name__ == "__main__":
    start_bot()
