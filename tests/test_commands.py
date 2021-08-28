"""
Test commands.py
"""

# Standard library imports
import os

# Third-party library imports
import pytest

# Local imports
from ugc import commands
from ugc.utils import commands_helpers


def test_generate_sample_does_not_overwrite_existing_location(
    local_config, tmpdir
):
    filename = ".ugc-grades.json"
    local_config.path = tmpdir / filename
    test_file = tmpdir.join(filename)
    test_file.write("content")  # file can't be empty to test it
    expected = {
        "ok": False,
        "error": f"Will not overwrite existing {local_config.path}",
    }
    assert commands.generate_sample(local_config) == expected


def test_generate_sample_creates_file_if_it_does_not_exist(
    local_config, tmpdir
):
    local_config.path = tmpdir / ".ugc-grades.json"
    result = commands.generate_sample(local_config)
    assert os.path.exists(local_config.path)
    assert result == {"ok": True, "error": None}


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
def test_get_module_score_rounded_up(
    final_score, final_weight, midterm_score, midterm_weight, expected_score
):
    module = {
        "final_score": final_score,
        "final_weight": final_weight,
        "midterm_score": midterm_score,
        "midterm_weight": midterm_weight,
    }
    assert (
        commands_helpers.get_module_score_rounded_up(module) == expected_score
    )


@pytest.mark.parametrize(
    "final_score,final_weight,midterm_score,midterm_weight,expected_score",
    [
        (92, 70, 30, 30, 39),  # midterm < 35, final > 40: FAIL, capped at 39
        (34, 50, 99, 50, 39),  # FAIL: capped at 39
        (38, 50, 39, 50, 39),  # 35 < midterm < 40 + 35 < final < 40: FAIL
        (35, 70, 49, 30, 39),  # FAIL (avg. < 40)
        (38, 70, 42, 30, 39),  # FAIL (avg. < 40)
        (40, 50, 40, 50, 40),  # OK...
        (35, 70, 50, 30, 40),  # OK (39.5 → 40)
    ],
)
def test_get_module_score_with_failing_module(
    final_score, final_weight, midterm_score, midterm_weight, expected_score
):
    module = {
        "final_score": final_score,
        "final_weight": final_weight,
        "midterm_score": midterm_score,
        "midterm_weight": midterm_weight,
    }
    assert (
        commands_helpers.get_module_score_rounded_up(module) == expected_score
    )


def test_check_score_accuracy_all_modules(local_grades):
    local_grades.config.data["Algorithms and Data Structures I"] = {
        "final_score": 99,
        "final_weight": 50,
        "midterm_score": 78.5,
        "midterm_weight": 50,
        "module_score": 88,
    }
    local_grades.config.data["Web Development"] = {
        "final_score": 90,
        "final_weight": 50,
        "midterm_score": 61,
        "midterm_weight": 50,
        "module_score": 77,
    }
    result = commands.check_score_accuracy(local_grades)
    expected_dict = {
        "Algorithms and Data Structures I": {"actual": 88, "expected": 89},
        "Web Development": {"actual": 77, "expected": 76},
    }
    assert result == expected_dict


def test_summarize_progress_shows_no_progress_when_none_exists(
    local_grades, capsys
):
    commands.summarize_progress(local_grades)
    captured = capsys.readouterr()
    assert captured.out == "No modules in progress.\n"


def test_summarize_done_shows_no_progress_when_none_exists(
    local_grades, capsys
):
    commands.summarize_done(local_grades)
    captured = capsys.readouterr()
    assert captured.out == "No modules done. Good luck in your journey!\n"


def test_summarize_all_shows_no_progress_when_none_exists(
    local_grades, capsys
):
    expected_output = """\
Modules completed
================================================================================
No modules done. Good luck in your journey!

Modules in progress
================================================================================
No modules in progress.
"""
    commands.summarize_all(local_grades)
    captured = capsys.readouterr()
    assert captured.out == expected_output
