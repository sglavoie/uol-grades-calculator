# Standard library imports
from datetime import datetime
from pathlib import Path
import calendar
import shutil

# Third-party library imports
from tabulate import tabulate
import click
import pandas as pd

# Local imports
from ugc.grades import Grades
from ugc.utils import mathtools
from ugc.utils import grades_helpers


def get_module_score_rounded_up(module) -> float:
    module_score = grades_helpers.get_module_score(module)
    return mathtools.round_half_up(module_score)


def there_are_no_modules_in_progress(grades) -> bool:
    if grades.get_list_of_modules_in_progress():
        return False
    click.secho("No modules in progress.", fg="bright_blue")
    return True


def print_modules_in_progress(pretty_printer, grades):
    click.secho("Modules in progress:", fg="bright_blue")
    pretty_printer.pprint(grades.get_list_of_modules_in_progress())


def print_weighted_average_in_progress(wavg, only_in_progress=False) -> None:
    msg = "only for" if only_in_progress else "including"

    wects = grades_helpers.get_ects_equivalent_score(wavg)
    wus = grades_helpers.get_us_letter_equivalent_score(wavg)

    click.secho(
        f"\nWeighted average ({msg} modules in progress): {wavg} (ECTS: {wects}, US: {wus})",
        fg="bright_green",
    )


def print_unweighted_average_in_progress(uavg, only_in_progress=False) -> None:
    msg = "only for" if only_in_progress else "including"

    uects = grades_helpers.get_ects_equivalent_score(uavg)
    uus = grades_helpers.get_us_letter_equivalent_score(uavg)

    click.secho(
        f"Unweighted average ({msg} modules in progress): {uavg} (ECTS: {uects}, US: {uus})",
        fg="bright_yellow",
    )


def generate_sample_copy_config_file_and_print_message(config_path: str):
    here = Path(__file__).parent  # directory containing this file
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

    # Drop unwanted columns (will take too much horizontal space). These
    # columns may not exist, so try dropping them one by one.
    for column in [
        "final_weight",
        "midterm_weight",
        "midterm_score",
        "final_score",
    ]:
        try:
            df_modules_taken = df_modules_taken.drop(
                column,
                axis=1,
            )
        except KeyError:
            pass

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


def dataframe_map_module_to_weight(row) -> int:
    """
    Return the weight of a given module from a dataframe row based on the
    module level and the module name (since the final project is worth more).

    Args:
        row (dataframe row): A row from a dataframe containing at least two
                             columns, `Level` and `Module name`.

    Returns:
        int: Integer value corresponding to the weight of a module.
    """
    if row["Level"] == 4:
        return 1
    if row["Level"] == 5:
        return 3
    if row["Level"] == 6 and row["Module name"] != "Final Project":
        return 5
    return 10  # final project is worth twice as much as any other L6


def dataframe_get_weighted_average(df, data_col, weight_col, by_col) -> float:
    """
    Calculate the weighted average in a dataframe from a numerical column
    and an integer column (weight) where the results are grouped by the column
    `by_col`.

    Args:
        df (DataFrame): Pandas dataframe, used to temporarily store new columns.
        data_col (number): int or float column from a dataframe.
        weight_col (number): int or float column from a dataframe.
        by_col ([type]): A dataframe column from which weights should be grouped.

    Returns:
        float: Weighted average calculated from `data_col` and `weight_col`
               and grouped by `by_col`.
    """
    df["_data_times_weight"] = df[data_col] * df[weight_col]
    df["_weight_where_notnull"] = df[weight_col] * pd.notnull(df[data_col])
    g = df.groupby(by_col)
    result = g["_data_times_weight"].sum() / g["_weight_where_notnull"].sum()
    del df["_data_times_weight"], df["_weight_where_notnull"]
    return result


def dataframe_parse_datetime_as_month_year(row) -> str:
    """
    Take in a dataframe row, get a timestamp from a column and return a
    formatted string in the form MMM YYYY, where MMM is the abbreviation
    of a month's name.

    Args:
        row: A dataframe row.

    Returns:
        str: A formatted string of the form "MMM YYYY".
    """
    date = str(row["Completion date"])[:10]  # slice YYYY-MM-DD only
    date = datetime.strptime(date, "%Y-%m-%d")
    year, month = date.year, date.month
    month_name = calendar.month_abbr[month]
    return f"{month_name} {year}"
