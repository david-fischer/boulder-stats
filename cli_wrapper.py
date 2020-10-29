#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from boulder_stats.cli import cli

if __name__ == "__main__":
    sys.argv[0] = "boulder_stats"  # re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(cli())
