"""
Manage the configuration file.
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import click
import yaml

# Local imports
from ugc.errors import ConfigValidationError


class Config:
    """Loads the configuration file where grades are stored."""

    def __init__(self, config_path=None):
        self.data = {}

        grades_template = Path(__file__).parent / "grades-template.yml"
        with open(grades_template) as gfile:
            self.default = yaml.safe_load(gfile)
            gfile.seek(0)  # need to reset position in file to read it again
            self.template = gfile.read().splitlines()
            self.template[1:] = [
                l.split(":")[0] + ":" for l in self.template[1:]
            ]

        if config_path is not None:
            self.path = config_path
        else:
            self.path = f"{str(Path.home())}/.grades.yml"

    def load(self) -> dict:
        """Load grades from a YAML file."""
        try:
            open(self.path)
        except FileNotFoundError:
            click.secho(
                f"Configuration file not found: {self.path}", fg="bright_red"
            )

        with open(self.path) as gfile:
            self.check_config_format_is_syntactically_correct()
            self.data = yaml.safe_load(gfile)
            self.verify()
            return self.data

    def verify(self) -> None:
        """Check that the config file contains valid data. One of the
        functions will throw an error if the config is not valid."""
        self.check_config_is_not_empty()
        self.check_total_weight_sums_up_100_in_all_modules()
        self.check_score_accuracy_raises_error_on_RPLed_module_with_scores()
        self.all_modules_are_found_with_valid_names()
        self.all_modules_are_set_to_correct_level()

    def check_config_is_not_empty(self) -> bool:
        if self.data is None:
            raise ConfigValidationError(
                f"Configuration file is empty ({self.path})."
            )
        return True

    def check_config_format_is_syntactically_correct(self) -> bool:
        """Just make it much less probable we will find garbage in an
        altered config. Avoids having to check for YAML syntax errors."""
        with open(self.path) as gfile:
            content = gfile.read().splitlines()

        for idx, line in enumerate(content):
            if not line.startswith(self.template[idx]):
                # Legacy situation here :)
                if (
                    line == "Numerical Mathematics:"
                    and self.template[idx] == "Computational Mathematics:"
                ):
                    continue
                raise ConfigValidationError(
                    f"Line {idx + 1} does not match "
                    f"the template. Expected '{self.template[idx]}', "
                    f"got '{line}'"
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
            if values.get("module_score") == -1:  # module RPLed
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
                module not in self.data.keys()
                and module != "Computational Mathematics"
            ):
                raise ConfigValidationError(
                    f"Module '{module}' not found in configuration file "
                    f"({self.path}). Make sure the spelling is correct."
                )
        for module in self.data.keys():
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
