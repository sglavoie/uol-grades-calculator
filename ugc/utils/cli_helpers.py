# Third-party library imports
import click

# Local imports
from ugc import __version__


def print_version(context, param, value):
    "Print the program version and exit."
    if not value or context.resilient_parsing:
        return
    click.echo(__version__)
    context.exit()
