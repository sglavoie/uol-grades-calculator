"""
Manage the configuration file.
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import yaml


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
                return self.config
        except FileNotFoundError:
            print(f"Configuration file not found: {self.path}")
            return None
