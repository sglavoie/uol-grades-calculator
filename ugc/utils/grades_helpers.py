from ugc.utils import commands_helpers


def get_weight_of(level: int) -> int:
    """Return the weight of a given `level`. The ratio is 1:3:5 for
    modules of L4:L5:L6 respectively."""
    if level == 4:
        return 1
    if level == 5:
        return 3
    if level == 6:
        return 5
    return 0


def score_is_valid(module_score: float) -> bool:
    """Check whether a given score is a valid numeric value.
    Return a Boolean value."""
    try:
        if (
            module_score is not None
            and isinstance(float(module_score), float)
            and (0 <= module_score <= 100 or module_score == -1)
        ):
            return True
    except (ValueError, TypeError):
        pass
    return False


def get_us_letter_equivalent_score(score: float) -> str:
    """Get the letter equivalent in the US grading system for a given
    score."""
    if score >= 93:
        return "A"
    if score >= 90:
        return "A-"
    if score >= 87:
        return "B+"
    if score >= 83:
        return "B"
    if score >= 80:
        return "B-"
    if score >= 77:
        return "C+"
    if score >= 73:
        return "C"
    if score >= 70:
        return "C-"
    if score >= 67:
        return "D+"
    if score >= 63:
        return "D"
    if score >= 60:
        return "D-"
    if score == -1:  # RPL: score is not applicable
        return "N/A"
    return "F"


def get_ects_equivalent_score(score: float) -> str:
    """Return the grade in the ECTS equivalent form.
    Range from A to E/F."""
    if score >= 70:
        return "A"
    if score >= 60:
        return "B"
    if score >= 50:
        return "C"
    if score >= 40:
        return "D"
    if score == -1:  # RPL: score is not applicable
        return "N/A"
    return "E/F"


def get_score_of_module_in_progress(module: dict) -> float:
    result = -1
    for values in module.values():
        if values.get("final_score") and values.get("midterm_score"):
            result = commands_helpers.get_module_score(values)
        elif values.get("final_score"):
            result = values["final_score"]
        elif values.get("midterm_score"):
            result = values["midterm_score"]
    return result


def get_total_weight_modules_finished(modules: list) -> float:
    levels = []
    final_project = False
    for module in modules:
        for name, value in module.items():
            if name.lower() == "final project":
                final_project = True
            level = value.get("level")
            module_score = value.get("module_score")
            if "module_score" in value and module_score >= 0:
                levels.append(get_weight_of(level))
    total_weight = sum(levels)

    if final_project:
        total_weight += 5
    return total_weight


def get_total_score_modules_finished(modules: list) -> float:
    total = 0
    for module in modules:
        for key, values in module.items():
            module_score = values.get("module_score")
            level = get_weight_of(values.get("level"))
            extra = 2 if key.lower() == "final project" else 1
            if "module_score" in values and module_score >= 0:
                try:
                    total += module_score * level * extra
                except TypeError:
                    pass
    return total


def get_total_weight_modules_in_progress(modules: list) -> float:
    levels = []
    final_project = False
    for module in modules:
        for name, value in module.items():
            if name.lower() == "final project":
                final_project = True
            level = value.get("level")
            levels.append(get_weight_of(level))
    total_weight = sum(levels)

    if final_project:
        total_weight += 5
    return total_weight


def get_total_score_modules_in_progress(modules: list) -> float:
    total = 0
    for module in modules:
        for key, values in module.items():
            final = values.get("final_score")
            midterm = values.get("midterm_score")
            level = get_weight_of(values.get("level"))
            extra = 2 if key.lower() == "final project" else 1
            if final is not None and midterm is not None:
                module_score = commands_helpers.get_module_score(values)
            elif final is not None:
                module_score = final
            elif midterm is not None:
                module_score = midterm
            else:
                module_score = -1
            try:
                total += module_score * level * extra
            except TypeError:
                pass
    return total


def get_uk_gpa(average) -> float:
    """Return the GPA as calculated in the UK."""
    result = 0
    if average >= 35:
        result = 1
    if average >= 40:
        result = 2
    if average >= 45:
        result = 2.3
    if average >= 50:
        result = 2.7
    if average >= 55:
        result = 3
    if average >= 60:
        result = 3.3
    if average >= 65:
        result = 3.7
    if average >= 70:
        result = 4
    return round(result, 2)


def get_us_gpa(average) -> float:
    """Return the GPA as calculated in the US."""
    result = 0
    if average >= 60:
        result = 0.7
    if average >= 63:
        result = 1
    if average >= 67:
        result = 1.3
    if average >= 70:
        result = 1.7
    if average >= 73:
        result = 2
    if average >= 77:
        result = 2.3
    if average >= 80:
        result = 2.7
    if average >= 83:
        result = 3
    if average >= 87:
        result = 3.3
    if average >= 90:
        result = 3.7
    if average >= 93:
        result = 4
    return round(result, 2)


def get_classification(average) -> str:
    """Return a string containing the classification of the student
    according to the Programme Specification."""
    if average >= 70:
        return "First Class Honours"
    if average >= 60:
        return "Second Class Honours [Upper Division]"
    if average >= 50:
        return "Second Class Honours [Lower Division]"
    if average >= 40:
        return "Third Class Honours"
    return "Fail"
