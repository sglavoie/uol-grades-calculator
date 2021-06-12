"""
Set up pytest fixtures for convenient testing.
"""

# Third-party library imports
import pathlib
import pytest

# Local imports
from ugc.config import Config
from ugc.grades import Grades

FIXTURE_CONFIG_PATH = (
    pathlib.Path().absolute() / "ugc/grades-template.yml"
)


@pytest.fixture(scope="function")
def local_grades():
    """Return an instance of the Grades class as a fixture available
    for a module."""
    return Grades(config_path=FIXTURE_CONFIG_PATH)


@pytest.fixture(scope="function")
def local_config():
    """Return an instance of the Config class as a fixture available
    for a module."""
    return Config(config_path=FIXTURE_CONFIG_PATH)


@pytest.fixture(scope="module")
def local_bad_config():
    """Return an instance of the Config class as a fixture available
    for the function."""
    config_path = (
        pathlib.Path().absolute() / "tests/fixtures/yaml/bad_config.yml"
    )
    return Config(config_path=config_path)
