"""
Set up pytest fixtures for convenient testing.
"""

# Third-party library imports
import pathlib
import pytest
import yaml

# Local imports
from ugc.config import Config
from ugc.grades import Grades

FIXTURE_GRADES_PATH = "tests/fixtures/yaml/grades.yml"
FIXTURE_BAD_CONFIG_PATH = "tests/fixtures/yaml/bad_format.yml"
FIXTURE_GRADES_LEVELS_PATH = "tests/fixtures/yaml/levels.yml"
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
def grades_levels():
    """Return a dict containing all the modules with their respective level."""
    with open(FIXTURE_GRADES_LEVELS_PATH) as lfile:
        return yaml.safe_load(lfile)


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

@pytest.fixture(scope="function")
def local_bad_config():
    """Return an instance of the Config class as a fixture available
    for the function."""
    config_path = pathlib.Path().absolute() / FIXTURE_BAD_CONFIG_PATH
    return Config(config_path=config_path)


@pytest.fixture(scope="module")
def grades_modules_in_progress():
    """Return an instance of the Grades class containing modules taken,
    including modules in progress."""
    config_path = (
        pathlib.Path().absolute() / FIXTURE_GRADES_MODULES_IN_PROGRESS_PATH
    )
    return Grades(config_path=config_path)
