# Local imports
from ugc.utils import mathtools


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

        return module_score
    except TypeError:
        return -1


def get_module_score_rounded_up(module) -> float:
    module_score = get_module_score(module)
    return mathtools.round_half_up(module_score)
