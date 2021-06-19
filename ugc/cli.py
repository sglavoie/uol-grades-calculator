"""
Describes the commands available from the terminal when running this tool.
"""

# Standard library imports
from functools import update_wrapper
from pathlib import Path

# Third-party library imports
import click

# Local imports
from ugc import commands
from ugc.grades import Grades
from ugc.utils import cli_helpers


pass_grades = click.make_pass_decorator(Grades, ensure=True)

# From https://click.palletsprojects.com/en/8.0.x/commands/#decorating-commands
# There might be a more elegant way to do this, but it works well...
# No function with the `run_if_config_exists` decorator will execute if the
# config file is missing AND `ctx` must be passed as the first parameter if used
def run_if_config_exists(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        # invoke command only when attribute `config_exists` is set to True
        if ctx.obj.config_exists:
            return ctx.invoke(f, ctx.obj, *args, **kwargs)
        return None

    return update_wrapper(new_func, f)


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=cli_helpers.print_version,
    expose_value=False,
    is_eager=True,
    help="Print the program version and exit.",
)
@click.option(
    "--config",
    default=f"{str(Path.home())}/.grades.yml",
    show_default=True,
    help="Custom path to config file.",
)
@click.pass_context
def cli(ctx, config):
    ctx.obj = Grades(config_path=config)


@cli.group()
def summarize():
    """Print a summary of the progress made so far."""


@summarize.command(name="all")
@pass_grades
@run_if_config_exists
def all_(ctx, grades):
    """Output includes modules done as well as those in progress."""
    commands.summarize_all(grades)


@summarize.command()
@pass_grades
@run_if_config_exists
def done(ctx, grades):
    """Output includes only modules that are done and dusted."""
    commands.summarize_done(grades)


@summarize.command()
@pass_grades
@run_if_config_exists
def progress(ctx, grades):
    """Output includes only modules that are in progress.

    In progress means there is no value provided for `module_score` yet
    for a given module."""
    commands.summarize_progress(grades)


@cli.command()
@click.option(
    "-f",
    "--force-overwrite",
    is_flag=True,
    help="Overwrite the existing config file, if any.",
)
@pass_grades
def generate_sample(grades, force_overwrite):
    """Generate a sample grades YAML config file."""
    commands.generate_sample(grades.config, force_overwrite=force_overwrite)


@cli.group()
def check():
    """Perform sanity checks against the results generated."""


@check.command()
@pass_grades
@run_if_config_exists
def score_accuracy(ctx, grades):
    """Check for rounding errors when averaging module score."""
    commands.check_score_accuracy(grades)
