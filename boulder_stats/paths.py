"""File paths."""

import os

base_path = os.path.abspath(os.path.dirname(__file__))

SECRET_PATH = os.path.join(base_path, "secrets.json")
HDF_PATH = os.path.join(base_path, "collected_data.h5")
