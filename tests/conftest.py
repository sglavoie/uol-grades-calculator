"""
Set up pytest fixtures for convenient testing.
"""
import sys

sys.path.insert(0, "../src")

# Third-party library imports
import pytest

# Local imports
from src.grades import Grades


@pytest.fixture(scope="module")
def grades():
    """Return an instance of the Grades class as a fixture available
    module-wise."""
    return Grades()
