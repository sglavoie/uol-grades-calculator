"""
List the commands available from the CLI: one per function.
"""

# Standard library imports
import os

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


def generate_sample(config) -> bool:
    """Generate a sample grades YAML config file."""
    if os.path.exists(config.path):
        click.secho(
            f"Will not overwrite existing {config.path}", fg="bright_yellow"
        )
        return False

    commands_helpers.generate_sample_copy_config_file_and_print_message(
        config_path=config.path
    )
    return True


def generate_sample_overwrite(config) -> None:
    """Generate a sample grades YAML config file: overwrite if it exists."""
    file_existed = os.path.exists(config.path)

    if file_existed:
        click.secho(f"Overwriting {config.path}", fg="bright_blue")
    else:
        click.secho(f"Creating {config.path}", fg="bright_blue")

    commands_helpers.generate_sample_copy_config_file_and_print_message(
        config_path=config.path
    )


def summarize_all(grades: object, symbol: str = "=", repeat: int = 80) -> None:
    """Print a summary of modules done and in progress."""
    click.secho("Modules completed", fg="bright_cyan")
    click.secho(symbol * repeat, fg="bright_cyan")
    summarize_done(grades)

    click.secho("\nModules in progress", fg="bright_cyan")
    click.secho(symbol * repeat, fg="bright_cyan")
    summarize_progress(grades)


def summarize_done(grades):
    """Print a summary of the progress made so far for modules that are done
    and dusted."""
    finished_modules = grades.get_list_of_finished_modules()

    if not finished_modules:
        click.secho(
            "No modules done. Good luck in your journey!", fg="bright_blue"
        )
        return
    modules = grades_helpers.get_grades_list_as_list_of_dicts(finished_modules)

    df = commands_helpers.get_modules_done_dataframe(grades, modules)
    commands_helpers.pprint_dataframe(df)

    # Store all the data we want to print
    wavg = grades.weighted_average
    uavg = grades.unweighted_average
    wects = grades_helpers.get_ects_equivalent_score(wavg)
    uects = grades_helpers.get_ects_equivalent_score(uavg)
    wus = grades_helpers.get_us_letter_equivalent_score(wavg)
    uus = grades_helpers.get_us_letter_equivalent_score(uavg)
    wclass = grades_helpers.get_classification(wavg)
    wgpa_us = grades_helpers.get_us_gpa(wavg)
    wgpa_uk = grades_helpers.get_uk_gpa(wavg)
    total_credits = grades.get_total_credits()
    pct_done = grades.get_percentage_degree_done()

    click.secho(
        f"\nWeighted average: {wavg} (ECTS: {wects}, US: {wus})",
        fg="bright_green",
    )
    click.secho(
        f"Unweighted average: {uavg} (ECTS: {uects}, US: {uus})",
        fg="bright_yellow",
    )

    click.secho(
        f"Classification (weighted): {wclass}",
        fg="bright_blue",
    )
    click.secho(
        f"GPA (weighted): {wgpa_us} US – {wgpa_uk} UK",
        fg="magenta",
    )

    click.secho(
        f"Total credits done: {total_credits} / 360 ({pct_done}%)",
        fg="cyan",
    )


def summarize_progress(grades):
    """Print a summary of only the modules that are currently in progress."""
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return

    df_all_scores, _ = commands_helpers.get_modules_in_progress_dataframe(
        grades
    )
    commands_helpers.pprint_dataframe(df_all_scores)

    wavg = grades.weighted_average_in_progress
    uavg = grades.unweighted_average_in_progress
    commands_helpers.print_weighted_average_in_progress(wavg)
    commands_helpers.print_unweighted_average_in_progress(uavg)


def summarize_progress_avg_progress_only(grades):
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return

    (
        df_all_scores,
        in_progress,
    ) = commands_helpers.get_modules_in_progress_dataframe(grades)
    commands_helpers.pprint_dataframe(df_all_scores)

    wavg = grades.weighted_average_in_progress_only
    uavg = grades.unweighted_average_in_progress_only

    # No need to display if there's only one module: there's no average
    # to calculate
    if len(in_progress) > 1:
        commands_helpers.print_weighted_average_in_progress(
            wavg, only_in_progress=True
        )
        commands_helpers.print_unweighted_average_in_progress(
            uavg, only_in_progress=True
        )
