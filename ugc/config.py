"""
Manage the configuration file.
"""

# Standard library imports
from pathlib import Path
import json

# Local imports
from ugc.utils import console


class ConfigValidationError(Exception):
    """Raised when there is an error in the config file."""

    def __init__(self, custom_msg):
        self.custom_msg = custom_msg
        super().__init__()

    def __str__(self):
        return f"{self.custom_msg}"


class Config:
    """Loads the configuration where grades are stored.

    If `json_str` is passed, load from a JSON string. Instead, if
    `config_path` is passed, load from a path. Else, try loading from a
    default configuration file."""

    def __init__(self, json_str=None, config_path=None):
        self.data = {}
        self.json = json_str

        grades_template = Path(__file__).parent / "grades-template.json"
        with open(grades_template, encoding="UTF-8") as gfile:
            self.default = json.load(gfile)

        if config_path is not None:
            self.path = config_path
        else:
            self.path = f"{str(Path.home())}/.ugc-grades.json"

    def load(self) -> dict:
        """Load grades from JSON (string or file)."""
        err_msg = "Could not load grades as a valid JSON input."
        if self.json is not None:
            try:
                self.data = json.loads(self.json)
                self.verify()
                return self.data
            except json.decoder.JSONDecodeError as e:
                raise ConfigValidationError(err_msg) from e
        try:
            with open(self.path, encoding="UTF-8") as gfile:
                self.data = json.load(gfile)
                self.verify()
                return self.data
        except FileNotFoundError as e:
            console.print(f"[red]Configuration file not found: {self.path}")
            console.print("[blue]Try `ugc generate-sample --help`")
            raise e
        except json.decoder.JSONDecodeError as e:
            raise ConfigValidationError(err_msg) from e

    def verify(self) -> None:
        """Check that the config file contains valid data. One of the
        functions will throw an error if the config is not valid."""
        self.config_is_a_dict()
        self.check_config_is_not_empty()
        self.all_modules_are_found_with_valid_names()
        self.all_modules_are_set_to_correct_level()
        self.all_modules_have_valid_float_scores_and_weights()
        self.check_score_accuracy_raises_error_on_RPLed_module_with_scores()
        self.check_total_weight_sums_up_100_in_all_modules()

    def config_is_a_dict(self) -> bool:
        if not isinstance(self.data, dict):
            raise ConfigValidationError(
                "Configuration file must be convertible to a Python"
                f" dictionary. Got: {self.data}"
            )
        return True

    def check_config_is_not_empty(self) -> bool:
        if self.data is None:
            raise ConfigValidationError(
                f"Configuration file is empty ({self.path})."
            )
        return True

    def check_total_weight_sums_up_100_in_all_modules(self) -> bool:
        for module, values in self.data.items():
            if not self._check_total_weight_sums_up_100_for_module(
                values, module
            ):
                return False
        return True

    def check_score_accuracy_raises_error_on_RPLed_module_with_scores(
        self,
    ) -> bool:
        for module, values in self.data.items():
            if values.get("module_score") != -1:  # module not RPLed
                continue
            fs = values.get("final_score")
            ms = values.get("midterm_score")
            if fs or ms:
                raise ConfigValidationError(
                    f"Module '{module}' is marked for RPL. No score "
                    f"should be given. Got final_score={fs}, "
                    f"midterm_score={ms}"
                )
        return True

    @staticmethod
    def _check_total_weight_sums_up_100_for_module(
        module, module_name
    ) -> bool:
        if not module.get("final_weight") and not module.get("midterm_weight"):
            return True  # missing both is OK

        if not module.get("final_weight"):
            raise ConfigValidationError(
                f"final_weight is missing for the module {module_name}"
            )
        if not module.get("midterm_weight"):
            raise ConfigValidationError(
                f"midterm_weight is missing for the module {module_name}"
            )

        final = module["final_weight"]
        midterm = module["midterm_weight"]

        if not isinstance(final, int) or not isinstance(midterm, int):
            raise ConfigValidationError(
                "midterm_weight and final_weight should be integers for the "
                f"module {module_name}"
            )

        total = final + midterm
        if total != 100:
            raise ConfigValidationError(
                f"midterm_weight ({midterm}) and final_weight ({final}) "
                f"should add up to 100 (not {total}) for "
                f"the module {module_name}"
            )

        return True

    def all_modules_are_found_with_valid_names(self) -> bool:
        all_modules = self.default.keys()
        for module in all_modules:
            if (
                module not in self.data
                and module != "Computational Mathematics"
            ):
                raise ConfigValidationError(
                    f"Module '{module}' not found in configuration file "
                    f"({self.path}). Make sure the spelling is correct."
                )
        for module in self.data:
            if module not in all_modules and module != "Numerical Mathematics":
                raise ConfigValidationError(
                    f"Module '{module}' not expected in "
                    f"configuration file ({self.path})."
                )
        return True

    def all_modules_are_set_to_correct_level(self):
        levels = {k: v["level"] for k, v in self.default.items()}
        for module, values in self.data.items():
            if module == "Numerical Mathematics":
                module = "Computational Mathematics"
            if (
                values is None
                or not values.get("level")
                or values["level"] != levels[module]
            ):
                raise ConfigValidationError(
                    f"Module '{module}' contains an invalid level value "
                    f"(expected '{levels[module]}')."
                )
        return True

    def all_modules_have_valid_float_scores_and_weights(self) -> bool:
        keys = (
            "final_score",
            "final_weight",
            "midterm_score",
            "midterm_weight",
            "module_score",
        )
        for module, values in self.data.items():
            for key in keys:
                value = values.get(key)

                # ignore None values here: they will be handled elsewhere
                # as part of other checks if necessary
                if value is None:
                    continue

                # only possible valid values are float and int
                if not isinstance(value, int) and not isinstance(value, float):
                    raise ConfigValidationError(
                        f"Module '{module}' contains an invalid value for "
                        f"'{key}': got '{value}'"
                    )

                # a value <0 or >100 will be rejected, but if it's the
                # module_score, it could be -1 if the module has been RPLed
                # (checked elsewhere in `verify` function above)
                value_out_of_bounds = (
                    value > 100 or value < 0 and key != "module_score"
                )
                module_score_out_of_bounds = (
                    key == "module_score"
                    and value > 100
                    or value < 0
                    and value != -1
                )
                if (value_out_of_bounds) or module_score_out_of_bounds:
                    raise ConfigValidationError(
                        f"Module '{module}' contains an invalid value for "
                        f"'{key}'. Got '{value}'."
                    )
        return True
