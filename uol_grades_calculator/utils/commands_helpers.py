# Local imports
from uol_grades_calculator.utils import mathtools


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
