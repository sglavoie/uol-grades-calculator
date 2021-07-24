# Standard library imports
from pathlib import Path
import shutil

# Third-party library imports
import click
import pandas as pd

# Local imports
from ugc.grades import Grades
from ugc.utils import mathtools
from ugc.utils import grades_helpers
from tabulate import tabulate


def get_module_score_rounded_up(module) -> float:
    module_score = grades_helpers.get_module_score(module)
    return mathtools.round_half_up(module_score)


def there_are_no_modules_in_progress(grades) -> bool:
    if not grades.get_list_of_modules_in_progress():
        click.secho("No modules in progress.", fg="bright_blue")
        return True
    return False


def print_modules_in_progress(pretty_printer, grades):
    click.secho("Modules in progress:", fg="bright_blue")
    pretty_printer.pprint(grades.get_list_of_modules_in_progress())


def print_weighted_average_in_progress(wavg, only_in_progress=False) -> None:
    msg = "including"
    if only_in_progress:
        msg = "only for"

    wects = grades_helpers.get_ects_equivalent_score(wavg)
    wus = grades_helpers.get_us_letter_equivalent_score(wavg)

    click.secho(
        f"\nWeighted average ({msg} modules in progress): {wavg} (ECTS: {wects}, US: {wus})",
        fg="bright_green",
    )


def print_unweighted_average_in_progress(uavg, only_in_progress=False) -> None:
    msg = "including"
    if only_in_progress:
        msg = "only for"

    uects = grades_helpers.get_ects_equivalent_score(uavg)
    uus = grades_helpers.get_us_letter_equivalent_score(uavg)

    click.secho(
        f"Unweighted average ({msg} modules in progress): {uavg} (ECTS: {uects}, US: {uus})",
        fg="bright_yellow",
    )


def generate_sample_copy_config_file_and_print_message(config_path: str):
    # The directory containing this file
    here = Path(__file__).parent
    template_location = here / "../grades-template.yml"

    shutil.copyfile(template_location, config_path)
    click.secho("→ Configuration file generated.", fg="bright_green")


def pprint_dataframe(dataframe):
    print(
        tabulate(dataframe, headers="keys", tablefmt="psql", showindex=False)
    )


def get_modules_done_dataframe(
    grades: Grades, finished_modules: list
) -> pd.DataFrame:
    df_modules_taken = pd.DataFrame(finished_modules)

    # Drop unwanted columns (will take too much horizontal space)
    df_modules_taken = df_modules_taken.drop(
        ["final_weight", "midterm_weight", "midterm_score", "final_score"],
        axis=1,
    )

    # Reorder remaining columns
    df_modules_taken = df_modules_taken[
        [
            "completion_date",
            "level",
            "module_name",
            "module_score",
        ]
    ]

    # Get grades in ECTS and US systems and put them into a DataFrame
    ects = grades.get_module_scores_of_finished_modules_for_system(
        system="ECTS"
    )
    us = grades.get_module_scores_of_finished_modules_for_system(system="US")
    data = {
        "module_name": list(ects),
        "ECTS": list(ects.values()),
        "US": list(us.values()),
    }
    df_letter_scores = pd.DataFrame(data)

    # Merge DataFrames by module name to display all scores at once
    df_all_scores = pd.merge(
        df_modules_taken, df_letter_scores, on="module_name", how="outer"
    )

    # Replace RPL modules (assigned a value of -1) with 'N/A'
    df_all_scores = df_all_scores.replace(-1, "N/A")

    # Sort chronologically, then by level and finally by module name so it's
    # easier to read from left to right
    df_all_scores = df_all_scores.sort_values(
        by=["completion_date", "level", "module_name"]
    )

    # Rename the columns
    df_all_scores.columns = [
        "Completion date",
        "Level",
        "Module name",
        "Score",
        "ECTS",
        "US",
    ]

    return df_all_scores


def get_modules_in_progress_dataframe(grades: Grades) -> tuple:
    in_progress = grades.get_list_of_modules_in_progress()
    in_progress = grades_helpers.get_grades_list_as_list_of_dicts(in_progress)

    df_in_progress = pd.DataFrame(in_progress)

    series_name = df_in_progress.pop("module_name")
    series_level = df_in_progress.pop("level")
    df_in_progress = pd.concat(
        [series_name, series_level, df_in_progress], axis=1
    )

    # Get grades in ECTS and US systems and put them into a DataFrame
    ects = grades.get_scores_of_modules_in_progress_for_system(system="ECTS")
    us = grades.get_scores_of_modules_in_progress_for_system(system="US")
    data = {
        "module_name": list(ects),
        "ECTS": list(ects.values()),
        "US": list(us.values()),
    }
    df_letter_scores = pd.DataFrame(data)

    # Merge DataFrames by module name to display all scores at once
    df_all_scores = pd.merge(
        df_in_progress, df_letter_scores, on="module_name", how="outer"
    )

    # Replace RPL modules (assigned a value of -1) with 'N/A'
    df_all_scores = df_all_scores.replace(-1, "N/A")

    # Sort by level, then by module name
    df_all_scores = df_all_scores.sort_values(by=["level", "module_name"])

    # Rename columns by iterating since we don't know which will be will there
    columns = df_all_scores.columns
    renamed = {"module_name": "Module name", "level": "Level"}
    for column in columns:
        if column == "midterm_score":
            renamed.update({"midterm_score": "Midterm"})
            df_all_scores = df_all_scores.drop(["midterm_weight"], axis=1)
        elif column == "final_score":
            renamed.update({"final_score": "Final"})
            df_all_scores = df_all_scores.drop(["final_weight"], axis=1)
    df_all_scores.rename(columns=renamed, inplace=True)

    return df_all_scores, in_progress
