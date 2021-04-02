"""
Manage the configuration file.
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import click
import yaml

# Local imports
from uol_grades_calculator.errors import ConfigValidationError


class Config:
    """Loads the configuration file where grades are stored."""

    def __init__(self, config_path=None):
        self.config = None
        if config_path is not None:
            self.path = config_path
        else:
            self.path = f"{str(Path.home())}/.grades.yml"

    def load(self) -> None:
        """Load grades from a YAML file."""
        try:
            with open(self.path) as gfile:
                self.config = yaml.safe_load(gfile)
                self.verify()
                return self.config
        except FileNotFoundError:
            click.secho(
                f"Configuration file not found: {self.path}", fg="bright_red"
            )
            return None

    def verify(self) -> bool:
        """Check that the config file contains valid data.
        Return True when it's valid, False otherwise."""
        conditions = [self.check_total_weight_sums_up_100_in_all_modules()]
        return all(conditions)

    def check_total_weight_sums_up_100_in_all_modules(self) -> bool:
        for module, values in self.config.items():
            if not self.check_total_weight_sums_up_100_for_module(
                values, module
            ):
                return False
        return True

    @staticmethod
    def check_total_weight_sums_up_100_for_module(module, module_name) -> bool:
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
