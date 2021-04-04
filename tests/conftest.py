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
FIXTURE_PARTIAL_GRADES_INACCURATE_PATH = (
    "tests/fixtures/yaml/partial_grades_inaccurate.yml"
)
FIXTURE_GRADES_MODULES_IN_PROGRESS_PATH = (
    "tests/fixtures/yaml/modules_in_progress.yml"
)


@pytest.fixture(scope="module")
def local_grades():
    """Return an instance of the Grades class as a fixture available
    for a module."""
    config_path = pathlib.Path().absolute() / FIXTURE_GRADES_PATH
    return Grades(config_path=config_path)


@pytest.fixture(scope="module")
def local_partial_grades_inaccurate():
    """Return an instance of the Grades class as a fixture with few UoL modules."""
    config_path = (
        pathlib.Path().absolute() / FIXTURE_PARTIAL_GRADES_INACCURATE_PATH
    )
    return Grades(config_path=config_path)


@pytest.fixture(scope="function")
def local_config():
    """Return an instance of the Config class as a fixture available
    for the function."""
    config_path = pathlib.Path().absolute() / FIXTURE_GRADES_PATH
    return Config(config_path=config_path)


@pytest.fixture(scope="module")
def grades_modules_in_progress():
    """Return an instance of the Grades class containing modules taken,
    including modules in progress."""
    config_path = (
        pathlib.Path().absolute() / FIXTURE_GRADES_MODULES_IN_PROGRESS_PATH
    )
    return Grades(config_path=config_path)
