"""
Set up pytest fixtures for convenient testing.
"""

# Third-party library imports
import pathlib
import pytest

# Local imports
from uol_grades_calculator.config import Config
from uol_grades_calculator.grades import Grades

FIXTURE_GRADES_PATH = "tests/fixtures/yaml/grades.yml"


@pytest.fixture(scope="module")
def local_grades():
    """Return an instance of the Grades class as a fixture available
    for a function."""
    config_path = pathlib.Path().absolute() / FIXTURE_GRADES_PATH
    return Grades(config_path=config_path)


@pytest.fixture(scope="function")
def local_config():
    """Return an instance of the Config class as a fixture available
    for the function."""
    config_path = pathlib.Path().absolute() / FIXTURE_GRADES_PATH
    return Config(config_path=config_path)
