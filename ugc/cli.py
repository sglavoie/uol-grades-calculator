"""
Describes the commands available from the terminal when running this tool.
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import click

# Local imports
from ugc import commands
from ugc.grades import Grades


pass_grades = click.make_pass_decorator(Grades, ensure=True)


@click.group()
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
def all_(grades):
    """Output includes modules done as well as those in progress."""
    commands.summarize_all(grades)


@summarize.command()
@pass_grades
def done(grades):
    """Output includes only modules that are done and dusted."""
    commands.summarize_done(grades)


@summarize.command()
@pass_grades
def progress(grades):
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
def score_accuracy(grades):
    """Check for rounding errors when averaging module score."""
    commands.check_score_accuracy(grades)
