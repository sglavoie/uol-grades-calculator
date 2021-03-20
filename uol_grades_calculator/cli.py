"""
Describes the commands available from the terminal when running this tool.
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import click

# Local imports
from uol_grades_calculator import commands
from uol_grades_calculator.grades import Grades


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


@cli.command()
@pass_grades
def summarize(grades):
    commands.summarize(grades)
