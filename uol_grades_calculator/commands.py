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
from uol_grades_calculator.utils import mathtools


def summarize(grades):
    """Print a summary of the progress made so far."""
    if not os.path.exists(grades.config.path):
        return

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


def generate_sample(config, force_overwrite=False) -> bool:
    """Generate a sample grades YAML config file."""
    if not force_overwrite and os.path.exists(config.path):
        print(f"Will not overwrite existing {config.path}")
        return False

    template = "uol_grades_calculator/grades-template.yml"
    template_location = Path().absolute() / template

    if force_overwrite:
        print(f"Overwriting {config.path}")

    shutil.copyfile(template_location, config.path)
    print("→ Configuration file generated.")
    return True


def check_score_accuracy_all_modules(grades) -> dict:
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

        expected_score = check_score_accuracy_module(values)
        actual_score = values["module_score"]
        if not expected_score == actual_score:
            expected_dict[module] = {
                "actual": actual_score,
                "expected": expected_score,
            }
            click.secho(
                f"{module}: {actual_score}% actual [expected {expected_score}%]",
                fg="red",
            )
    if not expected_dict:
        click.secho("All module scores are accurate!", fg="green")
    return expected_dict


def check_score_accuracy_module(module) -> float:
    try:
        final_score = module["final_score"]
        final_weight = module["final_weight"]
        midterm_score = module["midterm_score"]
        midterm_weight = module["midterm_weight"]
        module_score = (
            midterm_score * midterm_weight / 100
            + final_score * final_weight / 100
        )

        return mathtools.round_half_up(module_score)
    except TypeError:
        return -1
