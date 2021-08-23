"""
List the commands available from the CLI: one per function.
"""

# Standard library imports
from datetime import datetime
from pathlib import Path
import os
import sys

# Third-party library imports
import click
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Avoid overlap with annotations (auto placement of text)
from adjustText import adjust_text

# Local imports
from ugc.grades import Grades
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
        if expected_score != actual_score:
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
    if os.path.exists(config.path):
        click.secho(f"Overwriting {config.path}", fg="bright_blue")
    else:
        click.secho(f"Creating {config.path}", fg="bright_blue")

    commands_helpers.generate_sample_copy_config_file_and_print_message(
        config_path=config.path
    )


def plot_modules(grades: Grades, options: dict) -> None:
    """
    Plot modules over time with additional information and save the generated
    plot to `path`. It might be a good idea to refactor this gigantic function
    some day.

    Args:
        grades (Grades): ugc grades object.
    """
    # Set the stage by creating a dataframe to be used for plotting
    finished_modules = grades.get_list_of_finished_modules()

    if finished_modules:
        modules = grades_helpers.get_grades_list_as_list_of_dicts(
            finished_modules
        )
        df = commands_helpers.get_modules_done_dataframe(grades, modules)
    else:
        click.secho(
            "Aborting: there is not enough data to produce a plot.",
            fg="bright_blue",
        )
        sys.exit()

    # Drop unneeded columns
    df = df.drop(["ECTS", "US"], axis=1)

    # Convert column to datetime
    df["Completion date"] = pd.to_datetime(
        df["Completion date"], format="%Y-%m"
    )

    # Drop modules with invalid scores
    df = df.replace("N/A", np.NaN).dropna()

    # Get and set the weight for each module in a new column
    df["Weight"] = df.apply(
        commands_helpers.dataframe_map_module_to_weight, axis=1
    )

    # Set short module names so the graph is less cluttered
    df["Short name"] = df.apply(
        lambda row: grades.short_names[row["Module name"]], axis=1
    )

    # Set readable dates to be displayed on the x-axis
    df["Date string"] = df.apply(
        commands_helpers.dataframe_parse_datetime_as_month_year, axis=1
    )

    # Figure aspect ratio and output quality in dots per inch
    plt.figure(figsize=(12, 6), dpi=options["dpi"])

    # Graph title: if the `title` option is passed, set the title to that and
    # optionally append today's date if the `keep_date_in_title` option is set.
    today = datetime.today().strftime("%Y-%m-%d")
    if options.get("title") is not None:
        plot_title = options.get("title", "")
        if options.get("title_keep_date"):
            plot_title += f" ({today})"
    # Otherwise, contemplate the possibility of removing the date in the title.
    else:
        if not options.get("title_no_date"):
            plot_title = f"Grades over time as of {today}"
        else:
            plot_title = "Grades over time"
    plt.title(plot_title)

    # Store the annotations to be added to the graph (grades + module names)
    all_texts = []

    # Order in which colors will be applied
    colors = (
        "tab:blue",
        "tab:orange",
        "tab:purple",
        "tab:green",
        "tab:red",
        "m",
        "k",
    )

    # Give a different shape to the markers for each level in the degree
    level_shapes = ("o", "^", "s")

    # Iterate over each level in the degree
    groups = df.groupby("Level")
    for (name, group), color, shape in zip(groups, colors, level_shapes):
        texts = []
        plt.plot(
            group["Completion date"],
            group["Score"],
            color=color,
            marker=shape,
            linestyle="",
            label=name,
            alpha=1,
        )
        x = np.array(group["Completion date"])
        y = np.array(group["Score"])

        # With those options, there are no annotations to add, so just continue
        if options.get("no_module_names") and options.get("no_grades"):
            continue

        if options.get("long_module_names"):
            z = np.array(group["Module name"])
        else:
            z = np.array(group["Short name"])

        # When no module names are displayed, we only display the grades. But
        # when displaying the module names, check if we also want to display
        # the grades.
        if options.get("no_module_names"):
            texts = [
                (plt.text(x[i], y[i], f"{y[i]}")) for i, txt in enumerate(y)
            ]
        elif options.get("no_grades"):
            texts = [
                (plt.text(x[i], y[i], f"{z[i]}")) for i, txt in enumerate(y)
            ]
        else:
            texts = [
                (plt.text(x[i], y[i], f"{z[i]} ({y[i]})"))
                for i, txt in enumerate(y)
            ]

        all_texts.extend(texts)

    # Get the current value of the labels
    handles, labels = plt.gca().get_legend_handles_labels()

    # Will be used for the trend line and to determine whether we can plot
    # the other average lines
    dates = df.set_index("Completion date", append=False)
    dates = dates.index.to_julian_date()
    dates = dates.unique()

    # It's not much of a line with less than 2 different dates...
    if len(dates) < 2:
        click.secho(
            f"Not enough data to plot a line: skipping trend and averages...",
            fg="bright_yellow",
        )
    else:
        # Used to plot multiple lines, so calculate those once and for all
        weighted_average = commands_helpers.dataframe_get_weighted_average(
            df, "Score", "Weight", "Completion date"
        )
        average_over_time = df.groupby("Completion date").mean()

        if not options.get("no_avgs") and not options.get("no_avg_unweighted"):
            # Plot the unweighted average per semester
            plt.plot(
                average_over_time.index,
                average_over_time["Score"],
                color=colors[3],
                linestyle="solid",
                linewidth=1,
                alpha=0.8,
            )
            # Manually add the other lines we're plotting to the legend
            unweighted_semester = Line2D(
                [0],
                [0],
                color=colors[3],
                linestyle="solid",
                linewidth=1,
                alpha=0.8,
            )
            handles.extend([unweighted_semester])
            labels.extend(["Unweighted avg."])

        if not options.get("no_avgs") and not options.get("no_avg_weighted"):
            # Plot the weighted average per semester
            plt.plot(
                weighted_average.index,
                weighted_average,
                color=colors[4],
                linestyle="dashdot",
                linewidth=2,
                alpha=0.5,
            )
            weighted_semester = Line2D(
                [0],
                [0],
                color=colors[4],
                linestyle="dashdot",
                linewidth=2,
                alpha=0.5,
            )
            handles.extend([weighted_semester])
            labels.extend(["Weighted avg."])

        if not options.get("no_trend"):
            # Calculate the least squares polynomial fit and plot.
            # https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
            x = np.array(average_over_time.index)
            y = [round(v, 2) for v in np.array(average_over_time["Score"])]
            z = np.polyfit(dates, y, 1)
            p = np.poly1d(z)
            plt.plot(
                x,
                p(dates),
                linestyle="dotted",
                linewidth=3,
                alpha=0.4,
                color=colors[6],
            )
            trendline = Line2D(
                [0],
                [0],
                color=colors[6],
                linestyle="dotted",
                linewidth=3,
                alpha=0.4,
            )
            handles.extend([trendline])
            labels.extend(["Trend line"])

        if not options.get("no_avgs") and not options.get("no_avg_overall"):
            # Plot an horizontal line showing the weighted average obtained over time
            x = np.array(weighted_average.index)
            y = [round(v, 2) for v in np.array(weighted_average)]
            plt.plot(
                x,
                [round(weighted_average.mean(), 2)] * len(x),
                linestyle="solid",
                alpha=0.75,
                linewidth=1.25,
                color=colors[5],
            )
            weighted_degree = Line2D(
                [0], [0], color=colors[5], linestyle="solid", linewidth=1.25
            )
            handles.extend([weighted_degree])
            labels.extend(["Overall weighted avg."])

    # prepend with "Levels" to avoid adding a title to the legend
    labels = [f"Level {l}" if len(l) == 1 else l for l in labels]

    # Draw the legend outside the figure as it tends to overlap with data
    plt.legend(
        bbox_to_anchor=(1.3, 0.8),  # outside, top-right
        loc="upper right",
        shadow=True,
        borderaxespad=1,
        handles=handles,
        labels=labels,
    )

    # Add a grid for readability and increase precision by enabling minor ticks
    plt.grid(which="both", alpha=0.3, axis="y")
    plt.grid(which="major", alpha=0.3, axis="x")
    plt.minorticks_on()

    # Rotate the labels to take less space and label them from the
    # "Date string" column, which is easier to read
    plt.xticks(
        rotation=60,
        ticks=df["Completion date"].unique(),
        labels=df["Date string"].unique(),
    )

    # required to avoid overlap with labels in the figure
    adjust_text(all_texts)

    plt.tight_layout(pad=1)  # add some padding, otherwise the x-labels are cut

    # Save the results to the disk
    default_filename = today + "_grades_over_time.png"
    filename = (
        options.get("filename", "")
        if options.get("filename")
        else default_filename
    )

    # Make sure we save the file extension if it wasn't passed in the
    # `filename` option
    if not filename.endswith(".png"):
        filename += ".png"

    filepath = Path(os.getcwd()) / filename

    if options.get("path"):
        if not os.path.exists(options.get("path", "")):
            click.secho(
                f"Cannot save to the path specified: {Path(options.get('path', '')) / filename}",
                fg="bright_red",
            )
            click.secho(
                "Make sure the output directory exists.",
                fg="blue",
            )
            sys.exit()
        else:
            filepath = Path(options.get("path", "")) / filename

    if os.path.exists(filepath):
        click.secho(
            f"The output destination file already exists: {filepath}",
            fg="bright_yellow",
        )

        if not click.confirm(
            "Would you like to overwrite this file?",
            prompt_suffix=": ",
            show_default=True,
            err=False,
        ):
            click.secho(
                "Aborting: the existing file was kept intact.",
                fg="bright_blue",
            )
            sys.exit()

    try:
        plt.savefig(filepath)
        click.secho(f"Plot saved to {filepath}", fg="bright_green")
    except PermissionError:
        click.secho(
            f"PermissionError: could not save the output to {filepath}",
            fg="bright_red",
        )


def summarize_all(grades: Grades, symbol: str = "=", repeat: int = 80) -> dict:
    """Print a summary of modules done and in progress."""
    click.secho("Modules completed", fg="bright_cyan")
    click.secho(symbol * repeat, fg="bright_cyan")
    summary_done = summarize_done(grades)

    click.secho("\nModules in progress", fg="bright_cyan")
    click.secho(symbol * repeat, fg="bright_cyan")
    summary_progress = summarize_progress(grades)

    return {"done": summary_done, "progress": summary_progress}


def summarize_done(grades) -> dict:
    """Print a summary of the progress made so far for modules that are done
    and dusted."""
    if not (finished_modules := grades.get_list_of_finished_modules()):
        click.secho(
            "No modules done. Good luck in your journey!", fg="bright_blue"
        )
        return {}
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
    total_credits = grades.total_credits
    pct_done = grades.get_percentage_degree_done(total_credits)

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

    return {
        "modules": modules,
        "weighted_average": wavg,
        "unweighted_average": uavg,
        "weighted_ects": wects,
        "unweighted_ects": uects,
        "weighted_us": wus,
        "unweighted_us": uus,
        "weighted_class": wclass,
        "weighted_gpa_us": wgpa_us,
        "weighted_gpa_uk": wgpa_uk,
        "credits_done": total_credits,
        "percentage_done": pct_done,
    }


def summarize_progress(grades) -> dict:
    """Print a summary of only the modules that are currently in progress."""
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return {}

    (
        df_all_scores,
        in_progress,
    ) = commands_helpers.get_modules_in_progress_dataframe(grades)
    commands_helpers.pprint_dataframe(df_all_scores)

    wavg = grades.weighted_average_in_progress
    uavg = grades.unweighted_average_including_in_progress
    commands_helpers.print_weighted_average_in_progress(wavg)
    commands_helpers.print_unweighted_average_in_progress(uavg)

    return {
        "modules": in_progress,
        "weighted_average": wavg,
        "unweighted_average": uavg,
    }


def summarize_progress_avg_progress_only(grades) -> dict:
    if commands_helpers.there_are_no_modules_in_progress(grades):
        return {}

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

    return {
        "modules": in_progress,
        "weighted_average": wavg,
        "unweighted_average": uavg,
    }
