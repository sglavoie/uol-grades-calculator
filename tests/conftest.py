"""
Set up pytest fixtures for convenient testing.
"""

# Third-party library imports
import pytest

# Local imports
from uol_grades_calculator.config import Config
from uol_grades_calculator.grades import Grades


@pytest.fixture(scope="module")
def grades():
    """Return an instance of the Grades class as a fixture available
    module-wise."""
    return Grades()


@pytest.fixture(scope="module")
def config():
    """Return an instance of the Config class as a fixture available
    module-wise."""
    return Config()
