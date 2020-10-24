#!/usr/bin/env python3
"""This script provides the main function which serves as entry-point for setup.py."""
import pathlib
import sys

from fire import Fire

try:
    from .main import main
except ImportError:
    sys.path.append(pathlib.Path(__file__).parent.absolute())
    from main import main


def cli_main():
    """Entry point for setup.py."""
    Fire(main)


if __name__ == "__main__":
    cli_main()
