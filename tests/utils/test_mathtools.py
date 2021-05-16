"""
Test utils/mathtools.py
"""

# Third-party library imports
import pytest

# Local imports
from ugc.utils import mathtools


@pytest.mark.parametrize(
    "number,decimals,expected_value",
    [
        (12.5, 2, 12.5),
        (12.49999, 4, 12.5),
        (12.49999, 5, 12.49999),
        (12.5, 0, 13),
        (12.999, 0, 13),
        (0.5, 0, 1),
        (0, 0, 0),
    ],
)
def test_round_half_up(number, decimals, expected_value):
    result = mathtools.round_half_up(number, decimals)
    assert result == expected_value
