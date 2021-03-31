"""
List the commands available from the CLI: one per function.
"""

# Standard library imports
import os
from pathlib import Path
import pprint
import shutil


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
