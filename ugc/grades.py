"""
Command-line application to get information about progress made in a BSc
Computer Science at the University of London (calculations are specific
to this particular degree).
"""
# Local imports
from ugc.config import Config
from ugc.utils import (
    grades_helpers,
    mathtools,
)


class Grades:
    def __init__(
        self, json_str=None, config_path=None, verified=True, error=None
    ) -> None:
        """Set some default values before loading any grades."""
        self.error = error
        if not verified:
            self.config = Config()
            self.config_exists = False
            return
        if json_str is not None:
            # Load data from a JSON string instead of from a file
            self.config = Config(json_str=json_str)
        else:
            self.config = Config(config_path=config_path)

        # Return before raising an error with a config file not found
        # so we can run the `generate-sample` command.
        # Otherwise, trying to load the config file will unsurprisingly
        # not work...
        try:
            self.config.load()
        except FileNotFoundError:
            self.config_exists = False
            return
        self.config_exists = True

        self.data = self.config.load()
        self.short_names = grades_helpers.load_short_module_names()

    @property
    def weighted_average_in_progress_only(self) -> float:
        (
            modules_in_progress,
            weight_progress,
            score_progress,
        ) = self._get_weighted_data_of_modules_in_progress()
        return (
            0
            if not modules_in_progress
            else round(score_progress / weight_progress, 2)
        )

    @property
    def unweighted_average(self) -> float:
        """Return the unweighted average across all completed modules."""
        module_scores = self.get_module_scores_of_finished_modules()
        return (
            0
            if not module_scores
            else mathtools.round_half_up(
                sum(module_scores) / len(module_scores), 2
            )
        )

    @property
    def unweighted_average_including_in_progress(self) -> float:
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

    @property
    def unweighted_average_in_progress_only(self) -> float:
        """Return the unweighted average across modules in progress only."""
        (
            modules_in_progress,
            score_progress,
        ) = self._get_unweighted_data_of_modules_in_progress()
        return (
            0
            if not modules_in_progress
            else round(score_progress / len(modules_in_progress), 2)
        )

    @property
    def weighted_average(self) -> float:
        modules = self.get_list_of_finished_modules()
        module_scores = self.get_module_scores_of_finished_modules()
        total_weight = grades_helpers.get_total_weight_modules_finished(
            modules
        )
        total_score = grades_helpers.get_total_score_modules_finished(modules)

        return 0 if not module_scores else round(total_score / total_weight, 2)

    @property
    def weighted_average_in_progress(self) -> float:
        modules_finished = []
        modules_finished.extend(self.get_list_of_finished_modules())
        weight_finished = grades_helpers.get_total_weight_modules_finished(
            modules_finished
        )
        score_finished = grades_helpers.get_total_score_modules_finished(
            modules_finished
        )

        (
            modules_in_progress,
            weight_progress,
            score_progress,
        ) = self._get_weighted_data_of_modules_in_progress()

        modules_all = []
        modules_all.extend(modules_in_progress)
        modules_all.extend(modules_finished)

        total_weight = weight_finished + weight_progress
        total_score = score_finished + score_progress

        return 0 if not modules_all else round(total_score / total_weight, 2)

    @property
    def total_credits(self) -> int:
        """Get the total number of credits gotten so far as an integer."""
        total_credits = 0
        for subject_name, details in self.data.items():
            if details.get("module_score"):
                module_score = details["module_score"]
                if module_score == -1 or module_score >= 40:
                    # This won't be -1 but it does not matter
                    if subject_name.lower() == "final project":
                        total_credits += 30
                    else:
                        total_credits += 15
        return total_credits

    def _get_unweighted_data_of_modules_in_progress(self) -> tuple:
        modules_in_progress = []
        modules_in_progress.extend(self.get_list_of_modules_in_progress())
        score_progress = (
            grades_helpers.get_unweighted_total_score_modules_in_progress(
                modules_in_progress
            )
        )
        return modules_in_progress, score_progress

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
            if level and grades_helpers.score_is_valid(module_score):
                non_empty_values = {}
                for key, value in values.items():
                    if value is not None:
                        non_empty_values[key] = value
                modules.append({module: non_empty_values})
        return modules

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
                if not grades_helpers.score_is_valid(values["final_score"]):
                    continue
            else:
                values_to_skip.append("final_weight")
            if values.get("midterm_score"):
                if not grades_helpers.score_is_valid(values["midterm_score"]):
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
            result = grades_helpers.get_score_of_module_in_progress(module)
            modules_scores.append(result)

        return modules_scores

    def _get_weighted_data_of_modules_in_progress(self) -> tuple:
        modules_in_progress = []
        modules_in_progress.extend(self.get_list_of_modules_in_progress())
        weight_progress = grades_helpers.get_total_weight_modules_in_progress(
            modules_in_progress
        )
        score_progress = (
            grades_helpers.get_weighted_total_score_modules_in_progress(
                modules_in_progress
            )
        )
        return modules_in_progress, weight_progress, score_progress

    def get_num_of_finished_modules(self) -> int:
        """Return the number of modules completed with a score greater
        than or equal to zero as an integer."""
        total = 0
        for _, values in self.data.items():
            module_score = values.get("module_score")
            if grades_helpers.score_is_valid(module_score):
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
            to_run = grades_helpers.get_us_letter_equivalent_score
        else:
            to_run = grades_helpers.get_ects_equivalent_score
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
            to_run = grades_helpers.get_us_letter_equivalent_score
        else:
            to_run = grades_helpers.get_ects_equivalent_score
        for module in modules:
            module_name = list(module.keys())[0]
            result = grades_helpers.get_score_of_module_in_progress(module)
            converted_scores[module_name] = to_run(result)
        return converted_scores

    @staticmethod
    def get_percentage_degree_done(num_credits: int) -> float:
        """From the total number of credits, return the percentage done
        out of 360 credits."""
        if num_credits > 360:
            return 100  # one could take more modules, still completion is 100%
        if num_credits < 0:
            return -1  # can't be negative! Returns -1 as an error
        return round(num_credits / 360 * 100, 2)
