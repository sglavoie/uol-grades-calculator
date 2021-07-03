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

    click.secho("Modules completed", fg="cyan")
    click.secho(symbol * repeat, fg="cyan")
    summarize_done(grades)

    click.secho("\nModules in progress", fg="cyan")
    click.secho(symbol * repeat, fg="cyan")
    summarize_progress(grades)


def summarize_done(grades):
    """Print a summary of the progress made so far for modules that are done
    and dusted."""

    if not grades.get_list_of_finished_modules():
        click.secho(
            "No modules done. Good luck in your journey!", fg="bright_blue"
        )
        return

    pretty_printer = pprint.PrettyPrinter(indent=2)
    wavg = grades.weighted_average

    click.secho("Modules taken:", fg="bright_blue")
    pretty_printer.pprint(grades.get_list_of_finished_modules())
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

    commands_helpers.print_classification_equivalence_gpa(
        pretty_printer, grades, wavg
    )

    click.secho(
        f"Total credits done: {grades.get_total_credits()} / 360 "
        f"({grades.get_percentage_degree_done()}%)",
        fg="bright_blue",
    )


def summarize_progress(grades):
    """Print a summary of only the modules that are currently in progress."""
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return

    pretty_printer = pprint.PrettyPrinter(indent=2)

    commands_helpers.print_modules_in_progress(pretty_printer, grades)

    wavg = grades.weighted_average_in_progress
    commands_helpers.print_weighted_average_in_progress(wavg)

    uavg = grades.unweighted_average_in_progress
    commands_helpers.print_unweighted_average_in_progress(uavg)

    commands_helpers.print_classification_equivalence_gpa_in_progress(
        pretty_printer, grades, wavg
    )


def summarize_progress_avg_progress_only(grades):
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return

    pretty_printer = pprint.PrettyPrinter(indent=2)

    commands_helpers.print_modules_in_progress(pretty_printer, grades)

    wavg = grades.weighted_average_in_progress_only
    commands_helpers.print_weighted_average_in_progress(
        wavg, only_in_progress=True
    )

    uavg = grades.unweighted_average_in_progress_only
    commands_helpers.print_unweighted_average_in_progress(
        uavg, only_in_progress=True
    )

    commands_helpers.print_classification_equivalence_gpa_in_progress(
        pretty_printer, grades, wavg
    )
