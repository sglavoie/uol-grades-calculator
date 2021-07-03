"""
Test utils/mathtools.py
"""

# Third-party library imports
from hypothesis import given, settings
from hypothesis.strategies import integers, floats
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


@given(integers(), integers(min_value=11))
def test_hypothesis_round_half_up_with_integers_raises_ValueError_on_large_decimals(
    number, decimals
):
    with pytest.raises(ValueError):
        mathtools.round_half_up(number, decimals)


@given(integers(), integers(max_value=-1))
def test_hypothesis_round_half_up_with_integers_and_negative_decimals(
    number, decimals
):
    with pytest.raises(ValueError):
        mathtools.round_half_up(number, decimals)


@given(integers(max_value=1_000_000), integers(min_value=0, max_value=10))
@settings(max_examples=10)
def test_hypothesis_round_half_up_with_integers(number, decimals):
    mathtools.round_half_up(number, decimals)


@given(
    floats(min_value=1_000_001, max_value=1_000_001),
    integers(min_value=0, max_value=10),
)
@settings(max_examples=10)
def test_hypothesis_round_half_up_with_floats_raises_ValueError_on_large_number(
    number, decimals
):
    with pytest.raises(ValueError):
        mathtools.round_half_up(number, decimals)
