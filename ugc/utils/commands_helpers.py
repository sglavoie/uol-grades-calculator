# Standard library imports
from pathlib import Path
import shutil

# Local imports
from ugc.utils import mathtools
from ugc.utils import grades_helpers

# Third-party library imports
import click


def get_module_score(module) -> float:
    try:
        final_score = module["final_score"]
        final_weight = module["final_weight"]
        midterm_score = module["midterm_score"]
        midterm_weight = module["midterm_weight"]
        module_score = (
            midterm_score * midterm_weight / 100
            + final_score * final_weight / 100
        )

        if midterm_score < 35 or final_score < 35:
            return 39  # automatic FAIL

        return module_score
    except TypeError:
        return -1


def get_module_score_rounded_up(module) -> float:
    module_score = get_module_score(module)
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

    click.secho(
        f"\nWeighted average ({msg} modules in progress): {wavg}",
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


def print_unweighted_average_in_progress(uavg, only_in_progress=False) -> None:
    msg = "including"
    if only_in_progress:
        msg = "only for"

    click.secho(
        f"\nUnweighted average ({msg} modules in progress): {uavg}",
        fg="bright_green",
    )
    click.secho(
        f" ECTS: {grades_helpers.get_ects_equivalent_score(uavg)}",
        fg="bright_blue",
    )
    click.secho(
        f" US: {grades_helpers.get_us_letter_equivalent_score(uavg)}",
        fg="bright_yellow",
    )


def print_classification_equivalence_gpa(pretty_printer, grades, wavg):
    click.secho(
        f"\nClassification (weighted): {grades_helpers.get_classification(wavg)}",
        fg="bright_blue",
    )
    click.secho("\nECTS grade equivalence:", fg="bright_yellow")
    pretty_printer.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="ECTS")
    )
    click.secho("\nUS grade equivalence:", fg="bright_blue")
    pretty_printer.pprint(
        grades.get_module_scores_of_finished_modules_for_system(system="US")
    )
    click.secho(
        f"\nGPA (weighted): {grades_helpers.get_us_gpa(wavg)} US – "
        f"{grades_helpers.get_uk_gpa(wavg)} UK",
        fg="bright_yellow",
    )


def print_classification_equivalence_gpa_in_progress(
    pretty_printer, grades, wavg
):
    click.secho(
        f"\nClassification (weighted): {grades_helpers.get_classification(wavg)}",
        fg="bright_blue",
    )
    click.secho("\nECTS grade equivalence:", fg="bright_yellow")
    pretty_printer.pprint(
        grades.get_scores_of_modules_in_progress_for_system(system="ECTS")
    )
    click.secho("\nUS grade equivalence:", fg="bright_blue")
    pretty_printer.pprint(
        grades.get_scores_of_modules_in_progress_for_system(system="US")
    )
    click.secho(
        f"\nGPA (weighted): {grades_helpers.get_us_gpa(wavg)} US – "
        f"{grades_helpers.get_uk_gpa(wavg)} UK",
        fg="bright_yellow",
    )


def generate_sample_copy_config_file_and_print_message(config_path):
    # The directory containing this file
    here = Path(__file__).parent
    template_location = here / "../grades-template.yml"

    shutil.copyfile(template_location, config_path)
    click.secho("→ Configuration file generated.", fg="bright_green")
