"""
Test commands.py
"""

# Standard library imports
import os

# Third-party library imports
import pytest

# Local imports
from uol_grades_calculator import commands


def test_generate_sample_does_not_overwrite_existing_location(
    local_config, tmpdir
):
    local_config.path = tmpdir / ".grades.yml"
    test_file = tmpdir.join(".grades.yml")
    test_file.write("content")  # file can't be empty to test it
    assert not commands.generate_sample(local_config)


def test_generate_sample_creates_file_if_it_does_not_exist(
    local_config, tmpdir
):
    local_config.path = tmpdir / ".grades.yml"
    result = commands.generate_sample(local_config)
    print(local_config.path)
    assert os.path.exists(local_config.path)
    assert result


@pytest.mark.parametrize(
    "final_score,final_weight,midterm_score,midterm_weight,expected_score",
    [
        (92, 50, 98, 50, 95),  # same weight, no rounding
        (99, 50, 100, 50, 100),  # same weight, round up
        (62.5, 50, 72, 50, 67),  # same weight, round down
        (65, 30, 75, 70, 72),  # diff. weight, no rounding
        (80, 30, 72.5, 70, 75),  # diff. weight, round up
        (67.8, 30, 72.5, 70, 71),  # diff. weight, round down
        (None, 30, 72.5, 70, -1),  # missing final_score
        (67.8, None, 72.5, 70, -1),  # missing final_weight
        (67.8, 30, None, 70, -1),  # missing midterm_score
        (67.8, 30, 72.5, None, -1),  # missing midterm_weight
    ],
)
def test_check_score_accuracy_module(
    final_score, final_weight, midterm_score, midterm_weight, expected_score
):
    module = {
        "final_score": final_score,
        "final_weight": final_weight,
        "midterm_score": midterm_score,
        "midterm_weight": midterm_weight,
    }
    assert commands.check_score_accuracy_module(module) == expected_score


def test_check_score_accuracy_all_modules(local_partial_grades_inaccurate):
    result = commands.check_score_accuracy_all_modules(local_partial_grades_inaccurate)
    expected_dict = {
        "Algorithms and Data Structures I": {
            "actual": 88,
            "expected": 89
        },
        "Web Development": {
            "actual": 77,
            "expected": 76
        }
    }
    assert result == expected_dict
