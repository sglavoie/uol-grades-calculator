"""
Simple script to get information about progress made in a
BSc Computer Science at the University of London
(calculations are specific to this particular degree).
"""

# Standard library imports
import os

# Local imports
from uol_grades_calculator.config import Config
from uol_grades_calculator.utils import commands_helpers, mathtools


class Grades:
    def __init__(self, config_path=None) -> None:
        """Set some default values before loading any grades."""
        self.config = Config(config_path=config_path)
        self.data = self.config.load()
        self.total_credits = 0

        # Avoid running calculations if the config file is not found
        # Otherwise, this will throw errors when running some commands
        if os.path.exists(self.config.path):
            self.load()

    def load(self) -> None:
        """Perform basic calculations required for most commands."""
        self.unweighted_average = self.calculate_unweighted_average()
        self.unweighted_average_in_progress = (
            self.calculate_unweighted_average_in_progress()
        )
        self.weighted_average = self.calculate_weighted_average()
        self.weighted_average_in_progress = (
            self.calculate_weighted_average_in_progress()
        )
        self.total_credits = self.get_total_credits()

    def calculate_unweighted_average(self) -> float:
        """Return the unweighted average across all completed modules."""
        module_scores = self.get_module_scores_of_finished_modules()
        return (
            0
            if not module_scores
            else mathtools.round_half_up(
                sum(module_scores) / len(module_scores), 2
            )
        )

    def calculate_unweighted_average_in_progress(self) -> float:
        """Return the unweighted average across all completed modules and
        those in progress."""
        module_scores = self.get_module_scores_of_finished_modules()
        module_scores.extend(self.get_scores_of_modules_in_progress())
        return (
            0
            if not module_scores
            else mathtools.round_half_up(
                sum(module_scores) / len(module_scores), 2
            )
        )

    def get_module_scores_of_finished_modules(self) -> list:
        """Return a list of floats with the score obtained in each module."""
        modules = self.get_list_of_finished_modules()
        module_scores = []
        for module in modules:
            for value in module.values():
                module_score = value.get("module_score")
                if "module_score" in value and module_score >= 0:
                    module_scores.append(module_score)
        return module_scores

    def get_list_of_finished_modules(self) -> list:
        """Return a list of dicts containing information about all the modules
        that have a valid score (either -1 or 0 <= x <= 100)."""
        modules = []
        for module, values in self.data.items():
            module_score = values.get("module_score")
            level = values.get("level")
            if level and self.score_is_valid(module_score):
                non_empty_values = {}
                for key, value in values.items():
                    if value is not None:
                        non_empty_values[key] = value
                modules.append({module: non_empty_values})
        return modules

    @staticmethod
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

    def get_list_of_modules_in_progress(self) -> list:
        """Return a list of dict containing all the non-empty values of the
        modules in progress."""
        modules = []
        for module, values in self.data.items():
            if (
                # module_score should be empty
                values.get("module_score") is not None
                # we need at least a score to report
                or not (
                    values.get("final_score") or values.get("midterm_score")
                )
                # we need to know which level we are working with
                or not values.get("level")
                # we need to have at least one weight to do calculations
                or not (
                    values.get("final_weight") or values.get("midterm_weight")
                )
            ):
                continue  # reject invalid modules

            # second, skip modules with invalid scores
            values_to_skip = []  # no score, then don't keep the weight
            if values.get("final_score"):
                if not self.score_is_valid(values["final_score"]):
                    continue
            else:
                values_to_skip.append("final_weight")
            if values.get("midterm_score"):
                if not self.score_is_valid(values["midterm_score"]):
                    continue
            else:
                values_to_skip.append("midterm_weight")

            # third, store non-empty values of valid modules
            non_empty_values = {}
            for key, value in values.items():
                if value is not None and key not in values_to_skip:
                    non_empty_values[key] = value
            modules.append({module: non_empty_values})
        return modules

    def get_scores_of_modules_in_progress(self) -> list:
        """Return a list of floats with the score obtained in each module
        in progress."""
        modules = self.get_list_of_modules_in_progress()
        modules_scores = []
        for module in modules:
            result = self.get_score_of_module_in_progress(module)
            modules_scores.append(result)

        return modules_scores

    @staticmethod
    def get_score_of_module_in_progress(module: dict) -> float:
        for values in module.values():
            if values.get("final_score") and values.get("midterm_score"):
                result = commands_helpers.get_module_score(values)
            elif values.get("final_score"):
                result = values["final_score"]
            elif values.get("midterm_score"):
                result = values["midterm_score"]
        return result

    def calculate_weighted_average(self) -> float:
        modules = self.get_list_of_finished_modules()
        module_scores = self.get_module_scores_of_finished_modules()
        total_weight = self._get_total_weight_modules_finished(modules)
        total_score = self._get_total_score_modules_finished(modules)

        return 0 if not module_scores else round(total_score / total_weight, 2)

    def _get_total_weight_modules_finished(self, modules: list) -> float:
        levels = []
        final_project = False
        for module in modules:
            for name, value in module.items():
                if name.lower() == "final project":
                    final_project = True
                level = value.get("level")
                module_score = value.get("module_score")
                if "module_score" in value and module_score >= 0:
                    levels.append(self.get_weight_of(level))
        total_weight = sum(levels)

        if final_project:
            total_weight += 5
        return total_weight

    def _get_total_score_modules_finished(self, modules: list) -> float:
        total = 0
        for module in modules:
            for key, values in module.items():
                module_score = values.get("module_score")
                level = self.get_weight_of(values.get("level"))
                extra = 2 if key.lower() == "final project" else 1
                if "module_score" in values and module_score >= 0:
                    try:
                        total += module_score * level * extra
                    except TypeError:
                        pass
        return total

    def calculate_weighted_average_in_progress(self) -> float:
        modules_finished = []
        modules_finished.extend(self.get_list_of_finished_modules())
        weight_finished = self._get_total_weight_modules_finished(
            modules_finished
        )
        score_finished = self._get_total_score_modules_finished(
            modules_finished
        )

        modules_in_progress = []
        modules_in_progress.extend(self.get_list_of_modules_in_progress())
        weight_progress = self._get_total_weight_modules_in_progress(
            modules_in_progress
        )
        score_progress = self._get_total_score_modules_in_progress(
            modules_in_progress
        )

        modules_all = []
        modules_all.extend(modules_in_progress)
        modules_all.extend(modules_finished)

        total_weight = weight_finished + weight_progress
        total_score = score_finished + score_progress

        return 0 if not modules_all else round(total_score / total_weight, 2)

    def _get_total_weight_modules_in_progress(self, modules: list) -> float:
        levels = []
        final_project = False
        for module in modules:
            for name, value in module.items():
                if name.lower() == "final project":
                    final_project = True
                level = value.get("level")
                levels.append(self.get_weight_of(level))
        total_weight = sum(levels)

        if final_project:
            total_weight += 5
        return total_weight

    def _get_total_score_modules_in_progress(self, modules: list) -> float:
        total = 0
        for module in modules:
            for key, values in module.items():
                final = values.get("final_score")
                midterm = values.get("midterm_score")
                level = self.get_weight_of(values.get("level"))
                extra = 2 if key.lower() == "final project" else 1
                if final is not None and midterm is not None:
                    module_score = commands_helpers.get_module_score(values)
                elif final is not None:
                    module_score = final
                elif midterm is not None:
                    module_score = midterm
                try:
                    total += module_score * level * extra
                except TypeError:
                    pass
        return total

    @staticmethod
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

    def get_total_credits(self) -> int:
        """Get the total number of credits gotten so far as an integer."""
        self.total_credits = 0
        for subject_name, details in self.data.items():
            if details.get("module_score"):
                module_score = details["module_score"]
                if module_score == -1 or module_score >= 40:
                    # This won't be -1 but it does not matter
                    if subject_name.lower() == "final project":
                        self.total_credits += 30
                    else:
                        self.total_credits += 15
        return self.total_credits

    def get_num_of_finished_modules(self) -> int:
        """Return the number of modules completed with a score greater
        than or equal to zero as an integer."""
        total = 0
        for _, values in self.data.items():
            module_score = values.get("module_score")
            if self.score_is_valid(module_score):
                total += 1
        return total

    def get_module_scores_of_finished_modules_for_system(
        self, system: str = "US"
    ) -> dict:
        """Return a dictionary containing the converted ECTS score
        for each module."""
        finished_modules = self.get_list_of_finished_modules()
        converted_scores = {}
        if system == "US":
            to_run = self.get_us_letter_equivalent_score
        elif system == "ECTS":
            to_run = self.get_ects_equivalent_score
        for module in finished_modules:
            for module_name, module_score in module.items():
                converted_scores[module_name] = to_run(
                    module_score.get("module_score")
                )
        return converted_scores

    def get_scores_of_modules_in_progress_for_system(
        self, system: str = "US"
    ) -> dict:
        """Return a dictionary containing the converted ECTS score
        for each module in progress."""
        modules = self.get_list_of_modules_in_progress()
        converted_scores = {}
        if system == "US":
            to_run = self.get_us_letter_equivalent_score
        elif system == "ECTS":
            to_run = self.get_ects_equivalent_score
        for module in modules:
            module_name = list(module.keys())[0]
            result = self.get_score_of_module_in_progress(module)
            converted_scores[module_name] = to_run(result)
        return converted_scores

    def get_classification(self) -> str:
        """Return a string containing the classification of the student
        according to the Programme Specification."""
        if self.weighted_average >= 70:
            return "First Class Honours"
        if self.weighted_average >= 60:
            return "Second Class Honours [Upper Division]"
        if self.weighted_average >= 50:
            return "Second Class Honours [Lower Division]"
        if self.weighted_average >= 40:
            return "Third Class Honours"
        return "Fail"

    def get_classification_in_progress(self) -> str:
        """Return a string containing the classification of the student
        according to the Programme Specification, including modules in
        progress."""
        if self.weighted_average_in_progress >= 70:
            return "First Class Honours"
        if self.weighted_average_in_progress >= 60:
            return "Second Class Honours [Upper Division]"
        if self.weighted_average_in_progress >= 50:
            return "Second Class Honours [Lower Division]"
        if self.weighted_average_in_progress >= 40:
            return "Third Class Honours"
        return "Fail"

    def get_uk_gpa(self, in_progress=False) -> float:
        """Return the GPA as calculated in the UK."""
        average = self.weighted_average
        if in_progress:
            average = self.weighted_average_in_progress
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

    def get_us_gpa(self, in_progress=False) -> float:
        """Return the GPA as calculated in the US."""
        average = self.weighted_average
        if in_progress:
            average = self.weighted_average_in_progress
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

    @staticmethod
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

    @staticmethod
    def get_ects_equivalent_score(score: int) -> str:
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

    def get_percentage_degree_done(self) -> float:
        """From the total number of credits, return the percentage done
        out of 360 credits."""
        if self.total_credits > 360:
            return -1  # can't be more than what's available!
        return round(self.total_credits / 360 * 100, 2)
