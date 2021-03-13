"""
Describes the commands available from the terminal when running this tool.
"""

# Standard library imports
from pathlib import Path
import pprint

# Third-party library imports
import click

# Local imports
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
    """Print a summary of the progress made so far."""
    prettyp = pprint.PrettyPrinter(indent=2)
    print("Modules taken:")
    prettyp.pprint(grades.get_list_of_finished_modules())
    print("Number of modules done:", grades.get_num_of_finished_modules())
    print("Scores so far:", grades.get_module_scores_of_finished_modules())
    print(
        f"\nWeighted average: {grades.weighted_average}"
        f" (ECTS: {grades.get_ects_equivalent_score(grades.weighted_average)},"
        f" US: {grades.get_us_letter_equivalent_score(grades.weighted_average)})"
    )
    print(
        f"Unweighted average: {grades.unweighted_average}"
        f" (ECTS: {grades.get_ects_equivalent_score(grades.unweighted_average)},"
        f" US: {grades.get_us_letter_equivalent_score(grades.unweighted_average)})"
    )
    print("\nClassification:", grades.get_classification())
    print("\nECTS grade equivalence:")
    prettyp.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="ECTS")
    )
    print("\nUS grade equivalence:")
    prettyp.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="US")
    )
    print(f"\nGPA: {grades.get_us_gpa()} (US) – {grades.get_uk_gpa()} (UK)")
    print(
        f"Total credits done: {grades.get_total_credits()} / 360",
        f"({grades.get_percentage_degree_done()}%)",
    )
