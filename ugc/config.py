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
        self.config = {}
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
            self.config = yaml.safe_load(gfile)
            self.verify()
            return self.config

    def verify(self) -> None:
        """Check that the config file contains valid data. One of the
        functions will throw an error if the config is not valid."""
        self.check_total_weight_sums_up_100_in_all_modules()
        self.all_modules_are_found_with_valid_names()
        self.all_modules_are_set_to_correct_level()

    def check_config_format_is_syntactically_correct(self) -> bool:
        """Just make it much less probable we will find garbage in an
        altered config. Avoids having to check for YAML syntax errors."""
        grades_template = Path(__file__).parent / "grades-template.yml"
        with open(grades_template) as tfile:
            expected_start_lines = tfile.read().splitlines()
        expected_start_lines[1:] = [
            l.split(":")[0] + ":" for l in expected_start_lines[1:]
        ]

        with open(self.path) as gfile:
            content = gfile.read().splitlines()

        for idx, line in enumerate(content):
            if not line.startswith(expected_start_lines[idx]):
                # Legacy situation here :)
                if (
                    line == "Numerical Mathematics:"
                    and expected_start_lines[idx]
                    == "Computational Mathematics"
                ):
                    continue
                raise ConfigValidationError(
                    f"Line {idx + 1} does not match "
                    f"the template. Expected '{expected_start_lines[idx]}', "
                    f"got '{line}'"
                )
        return True

    def check_total_weight_sums_up_100_in_all_modules(self) -> bool:
        for module, values in self.config.items():
            if not self._check_total_weight_sums_up_100_for_module(
                values, module
            ):
                return False
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
        all_modules = [
            "Algorithms and Data Structures I",
            "Computational Mathematics",
            "Discrete Mathematics",
            "Fundamentals of Computer Science",
            "How Computers Work",
            "Introduction to Programming I",
            "Introduction to Programming II",
            "Web Development",
            "Algorithms and Data Structures II",
            "Agile Software Projects",
            "Computer Security",
            "Databases Networks and the Web",
            "Graphics Programming",
            "Object Oriented Programming",
            "Programming with Data",
            "Software Design and Development",
            "Databases and Advanced Data Techniques",
            "Machine Learning and Neural Networks",
            "Artificial Intelligence",
            "Intelligent Signal Processing",
            "Natural Language Processing",
            "Data Science",
            "Final Project",
        ]
        for module in all_modules:
            if (
                module not in self.config.keys()
                and module != "Computational Mathematics"
            ):
                raise ConfigValidationError(
                    f"Module '{module}' not found in configuration file"
                    f"({self.path}). Make sure the spelling is correct."
                )
        for module in self.config.keys():
            if module not in all_modules and module != "Numerical Mathematics":
                raise ConfigValidationError(
                    f"Module '{module}' not expected in"
                    f"configuration file ({self.path})."
                )
        return True

    def all_modules_are_set_to_correct_level(self):
        levels = {
            "Algorithms and Data Structures I": 4,
            "Computational Mathematics": 4,
            "Discrete Mathematics": 4,
            "Fundamentals of Computer Science": 4,
            "How Computers Work": 4,
            "Introduction to Programming I": 4,
            "Introduction to Programming II": 4,
            "Web Development": 4,
            "Agile Software Projects": 5,
            "Algorithms and Data Structures II": 5,
            "Computer Security": 5,
            "Databases Networks and the Web": 5,
            "Graphics Programming": 5,
            "Object Oriented Programming": 5,
            "Programming with Data": 5,
            "Software Design and Development": 5,
            "Artificial Intelligence": 6,
            "Data Science": 6,
            "Databases and Advanced Data Techniques": 6,
            "Intelligent Signal Processing": 6,
            "Machine Learning and Neural Networks": 6,
            "Natural Language Processing": 6,
            "Final Project": 6,
        }
        for module, values in self.config.items():
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
