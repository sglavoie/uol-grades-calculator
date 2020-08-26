import sys

sys.path.insert(0, "../src")

# Third-party library imports
import pytest

# Local imports
from src.grades import Grades


@pytest.fixture(scope="module")
def grades():
    return Grades()
