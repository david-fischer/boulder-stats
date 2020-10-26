#!/usr/bin/env python3
"""This script provides the main function which serves as entry-point for setup.py."""


from fire import Fire

from scheduler import start_data_collection
from telegram_bot import start_bot


def cli_main():
    """Entry point for setup.py."""
    Fire({"start_bot": start_bot, "collect_data": start_data_collection})


if __name__ == "__main__":
    cli_main()
