"""
List the commands available from the CLI: one per function.
"""

# Standard library imports
import os
from pathlib import Path
import pprint
import shutil

# Third-party library imports
import click

# Local imports
from ugc.utils import commands_helpers, grades_helpers


def check_score_accuracy(grades) -> dict:
    if not os.path.exists(grades.config.path):
        return {}

    expected_dict = {}
    for module, values in grades.data.items():
        conditions = [
            values.get("final_score"),
            values.get("final_weight"),
            values.get("midterm_score"),
            values.get("midterm_weight"),
            values.get("module_score"),
        ]
        if not all(conditions):
            continue

        expected_score = commands_helpers.get_module_score_rounded_up(values)
        actual_score = values["module_score"]
        if not expected_score == actual_score:
            expected_dict[module] = {
                "actual": actual_score,
                "expected": expected_score,
            }
            click.secho(
                f"{module}: {actual_score}% actual [expected {expected_score}%]",
                fg="bright_red",
            )
    if not expected_dict:
        click.secho("All module scores are accurate!", fg="bright_green")
    return expected_dict


def generate_sample(config, force_overwrite=False) -> bool:
    """Generate a sample grades YAML config file."""
    if not force_overwrite and os.path.exists(config.path):
        click.secho(
            f"Will not overwrite existing {config.path}", fg="bright_yellow"
        )
        return False

    # The directory containing this file
    here = Path(__file__).parent
    template_location = here / "grades-template.yml"

    if force_overwrite:
        click.secho(f"Overwriting {config.path}", fg="bright_blue")

    shutil.copyfile(template_location, config.path)
    click.secho("→ Configuration file generated.", fg="bright_green")
    return True


def summarize_all(grades: object, symbol: str = "=", repeat: int = 60) -> None:
    """Print a summary of modules done and in progress."""
    if not os.path.exists(grades.config.path):
        return

    click.secho("Modules completed", fg="cyan")
    click.secho(symbol * repeat, fg="cyan")
    summarize_done(grades)

    click.secho("\nModules in progress", fg="cyan")
    click.secho(symbol * repeat, fg="cyan")
    summarize_progress(grades)


def summarize_done(grades):
    """Print a summary of the progress made so far for modules that are done
    and dusted."""
    if not os.path.exists(grades.config.path):
        return

    prettyp = pprint.PrettyPrinter(indent=2)
    wavg = grades.weighted_average

    click.secho("Modules taken:", fg="bright_blue")
    prettyp.pprint(grades.get_list_of_finished_modules())
    click.secho(
        f"Number of modules done: {grades.get_num_of_finished_modules()}",
        fg="bright_yellow",
    )
    click.secho(
        f"Scores so far: {grades.get_module_scores_of_finished_modules()}",
        fg="bright_blue",
    )
    click.secho(f"\nWeighted average: {wavg}", fg="bright_green")
    click.secho(
        f" ECTS: {grades_helpers.get_ects_equivalent_score(wavg)}",
        fg="bright_blue",
    )
    click.secho(
        f" US: {grades_helpers.get_us_letter_equivalent_score(wavg)}",
        fg="bright_yellow",
    )
    click.secho(
        f"\nUnweighted average: {grades.unweighted_average}", fg="bright_green"
    )
    click.secho(
        f" ECTS: {grades_helpers.get_ects_equivalent_score(grades.unweighted_average)}",
        fg="bright_blue",
    )
    click.secho(
        f" US: {grades_helpers.get_us_letter_equivalent_score(grades.unweighted_average)}",
        fg="bright_yellow",
    )
    click.secho(
        f"\nClassification (weighted): {grades_helpers.get_classification(wavg)}",
        fg="bright_blue",
    )
    click.secho("\nECTS grade equivalence:", fg="bright_yellow")
    prettyp.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="ECTS")
    )
    click.secho("\nUS grade equivalence:", fg="bright_blue")
    prettyp.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="US")
    )
    click.secho(
        f"\nGPA (weighted): {grades_helpers.get_us_gpa(wavg)} US – "
        f"{grades_helpers.get_uk_gpa(wavg)} UK",
        fg="bright_yellow",
    )
    click.secho(
        f"Total credits done: {grades.get_total_credits()} / 360 "
        f"({grades.get_percentage_degree_done()}%)",
        fg="bright_blue",
    )


def summarize_progress(grades):
    """Print a summary of only the modules that are currently in progress."""
    if not os.path.exists(grades.config.path):
        return

    prettyp = pprint.PrettyPrinter(indent=2)
    click.secho("Modules in progress:", fg="bright_blue")
    prettyp.pprint(grades.get_list_of_modules_in_progress())

    wavg = grades.weighted_average_in_progress
    click.secho(
        f"\nWeighted average (including modules in progress): {wavg}",
        fg="bright_green",
    )
    click.secho(
        f" ECTS: {grades_helpers.get_ects_equivalent_score(wavg)}",
        fg="bright_blue",
    )
    click.secho(
        f" US: {grades_helpers.get_us_letter_equivalent_score(wavg)}",
        fg="bright_yellow",
    )

    uavg = grades.unweighted_average_in_progress
    click.secho(
        f"\nUnweighted average (including modules in progress): {uavg}",
        fg="bright_green",
    )  # DONE
    click.secho(
        f" ECTS: {grades_helpers.get_ects_equivalent_score(uavg)}",
        fg="bright_blue",
    )
    click.secho(
        f" US: {grades_helpers.get_us_letter_equivalent_score(uavg)}",
        fg="bright_yellow",
    )
    click.secho(
        f"\nClassification (weighted): {grades_helpers.get_classification(wavg)}",
        fg="bright_blue",
    )
    click.secho("\nECTS grade equivalence:", fg="bright_yellow")
    prettyp.pprint(
        grades.get_scores_of_modules_in_progress_for_system(system="ECTS")
    )
    click.secho("\nUS grade equivalence:", fg="bright_blue")
    prettyp.pprint(
        grades.get_scores_of_modules_in_progress_for_system(system="US")
    )
    click.secho(
        f"\nGPA (weighted): {grades_helpers.get_us_gpa(wavg)} US – "
        f"{grades_helpers.get_uk_gpa(wavg)} UK",
        fg="bright_yellow",
    )
