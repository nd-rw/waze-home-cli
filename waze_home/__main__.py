"""Main entry point for the CLI application."""

import sys
from .cli import cli

if __name__ == "__main__":
    sys.exit(cli())