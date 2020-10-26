#!/usr/bin/env python3
"""This script provides the main function which serves as entry-point for setup.py."""
import os
import sys
from fire import Fire

# WORKAROUND TO MAKE THE RELATIVE IMPORTS WORK IF THE SCRIPT IS CALLED DIRECTLY:
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "boulder_stats"  # pylint: disable= redefined-builtin

from .scheduler import start_data_collection  # pylint: disable=wrong-import-position
from .telegram_bot import start_bot  # pylint: disable=wrong-import-position


def cli_main():
    """Entry point for setup.py."""
    Fire({"start_bot": start_bot, "collect_data": start_data_collection})


if __name__ == "__main__":
    cli_main()
