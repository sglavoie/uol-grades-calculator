"""
Simple script to get information about progress made in a
BSc Computer Science at the University of London
(calculations are specific to this particular degree).
"""

# Standard library imports
import json
import pprint

# Local imports
from .utils import mathtools


class Grades:
    """Provides methods to get insight about your grades."""

    def __init__(self) -> None:
        """Set some default values before loading any grades."""
        self.grades = None
        self.average = 0
        self.total_credits = 0

    def load(self, grades_file: str = "grades.json") -> None:
        """Load grades from a JSON file."""
        try:
            with open(grades_file) as grades_json:
                self.grades = json.load(grades_json)
        except FileNotFoundError as fnf:
            raise FileNotFoundError(
                f"\n\n{grades_file} was not found.\n"
            ) from fnf
        except json.decoder.JSONDecodeError as err:
            print(f"\n\n{grades_file} is not formatted correctly.\n")
            raise err
        else:  # no exception raised in `try` block
            self.average = self.calculate_average_of_finished_modules()
            self.total_credits = self.get_total_credits()

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

    @staticmethod
    def score_is_valid(score: float) -> bool:
        """Check whether a given score is a valid numeric value.
        Return a Boolean value."""
        try:
            if (
                score is not None
                and isinstance(float(score), float)
                and (0 <= score <= 100 or score == -1)
            ):
                return True
        except (ValueError, TypeError):
            pass
        return False

    def get_num_of_finished_modules(self) -> int:
        """Return the number of modules completed with a score greater
        than or equal to zero as an integer."""
        total = 0
        for _, values in self.grades.items():
            score = values.get("score")
            if self.score_is_valid(score):
                total += 1
        return total

    def get_list_of_finished_modules(self) -> list:
        """Return a list of dicts containing information about all the modules
        that have a valid score (either -1 or >= 0)."""
        modules = []
        for module, values in self.grades.items():
            score = values.get("score")
            if self.score_is_valid(score):
                modules.append({module: values})
        return modules

    def get_scores_of_finished_modules(self) -> list:
        """Return a list of floats with the score obtained in each module."""
        modules = self.get_list_of_finished_modules()
        scores = []
        for module in modules:
            for value in module.values():
                score = value.get("score")
                if "score" in value and score >= 0:
                    scores.append(score)
        return scores

    def get_scores_of_finished_modules_for_system(
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
                    module_score.get("score")
                )
        return converted_scores

    def calculate_average_of_finished_modules(self) -> float:
        """Return the unweighted average across all completed modules."""
        scores = self.get_scores_of_finished_modules()
        if len(scores) == 0:
            return 0
        return mathtools.round_half_up(sum(scores) / len(scores), 2)

    def get_classification(self) -> str:
        """Return a string containing the classification of the student
        according to the Programme Specification."""
        if self.average >= 70:
            return "First Class Honours"
        if self.average >= 60:
            return "Second Class Honours [Upper Division]"
        if self.average >= 50:
            return "Second Class Honours [Lower Division]"
        if self.average >= 40:
            return "Third Class Honours"
        return "Fail"

    def get_uk_gpa(self) -> float:
        """Return the GPA as calculated in the UK."""
        result = 0
        if self.average >= 35:
            result = 1
        if self.average >= 40:
            result = 2
        if self.average >= 45:
            result = 2.3
        if self.average >= 50:
            result = 2.7
        if self.average >= 55:
            result = 3
        if self.average >= 60:
            result = 3.3
        if self.average >= 65:
            result = 3.7
        if self.average >= 70:
            result = 4
        return round(result, 2)

    def get_us_gpa(self) -> float:
        """Return the GPA as calculated in the US."""
        result = 0
        if self.average >= 60:
            result = 0.7
        if self.average >= 63:
            result = 1
        if self.average >= 67:
            result = 1.3
        if self.average >= 70:
            result = 1.7
        if self.average >= 73:
            result = 2
        if self.average >= 77:
            result = 2.3
        if self.average >= 80:
            result = 2.7
        if self.average >= 83:
            result = 3
        if self.average >= 87:
            result = 3.3
        if self.average >= 90:
            result = 3.7
        if self.average >= 93:
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

    def get_total_credits(self) -> int:
        """Get the total number of credits gotten so far as an integer."""
        self.total_credits = 0
        for subject_name, details in self.grades.items():
            if details.get("score"):
                score = details["score"]
                if score == -1 or score >= 40:
                    # This won't be -1 but it does not matter
                    if subject_name.lower() == "final project":
                        self.total_credits += 30
                    else:
                        self.total_credits += 15
        return self.total_credits

    def get_percentage_degree_done(self) -> float:
        """From the total number of credits, return the percentage done
        out of 360 credits."""
        if self.total_credits > 360:
            return -1  # can't be more than what's available!
        return round(self.total_credits / 360 * 100, 2)


def main():
    """Execute the main functions of the script. Allows to be called from
    other modules."""
    prettyp = pprint.PrettyPrinter(indent=2, width=10)
    grades = Grades()
    grades.load()
    print("Modules taken:")
    prettyp.pprint(grades.get_list_of_finished_modules())
    print("Number of modules done:", grades.get_num_of_finished_modules())
    print("Scores so far:", grades.get_scores_of_finished_modules())
    print(
        f"Average so far: {grades.average}"
        f" (ECTS: {grades.get_ects_equivalent_score(grades.average)},"
        f" US: {grades.get_us_letter_equivalent_score(grades.average)})"
    )
    print("Classification:", grades.get_classification())
    print("ECTS grade equivalence:")
    prettyp.pprint(
        grades.get_scores_of_finished_modules_for_system(system="ECTS")
    )
    print("US grade equivalence:")
    prettyp.pprint(
        grades.get_scores_of_finished_modules_for_system(system="US")
    )
    print(f"GPA: {grades.get_us_gpa()} (US) – {grades.get_uk_gpa()} (UK)")
    print(
        f"Total credits done: {grades.get_total_credits()} / 360",
        f"({grades.get_percentage_degree_done()}%)",
    )


if __name__ == "__main__":
    main()
