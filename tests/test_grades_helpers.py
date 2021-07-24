# Third-party library imports
import pytest

# Local imports
from ugc.utils import grades_helpers


@pytest.mark.parametrize(
    "level,expected_weight",
    [
        (4, 1),
        (5, 3),
        (6, 5),
        (2, 0),
        (7, 0),
        (-1, 0),
        (0, 0),
        ("string", 0),
        ("", 0),
        ("1", 0),
        (2.2, 0),
        ([], 0),
        ({}, 0),
        (set(), 0),
    ],
)
def test_weight_level_of_module(level, expected_weight):
    """Check that the correct weight is given to each level.
    Level 4 should return 1.
    Level 5 should return 3.
    Level 6 should return 5.
    Anything else should return 0.
    """
    assert grades_helpers.get_weight_of(level) == expected_weight


@pytest.mark.parametrize(
    "module_score,expected_bool",
    [
        (61.5, True),
        (100, True),
        (0, True),
        (-1, True),
        (101, False),
        ("string", False),
        ({1, 2, 3}, False),
        ({"a": 1}, False),
        ([1, 2, 3], False),
        (-2, False),
        ({}, False),
        ("", False),
        (set(), False),
        (None, False),
    ],
)
def test_grades_module_scores_are_valid(module_score, expected_bool):
    assert grades_helpers.score_is_valid(module_score) == expected_bool


@pytest.mark.parametrize(
    "module_score,expected_module_score",
    [
        (100, "A"),
        (93, "A"),
        (92, "A-"),
        (90, "A-"),
        (89, "B+"),
        (87, "B+"),
        (86, "B"),
        (83, "B"),
        (82, "B-"),
        (80, "B-"),
        (79, "C+"),
        (77, "C+"),
        (76, "C"),
        (73, "C"),
        (72, "C-"),
        (70, "C-"),
        (69, "D+"),
        (67, "D+"),
        (66, "D"),
        (63, "D"),
        (62, "D-"),
        (60, "D-"),
        (59, "F"),
        (0, "F"),
        (-1, "N/A"),
    ],
)
def test_us_letter_equivalent_score(module_score, expected_module_score):
    assert (
        grades_helpers.get_us_letter_equivalent_score(module_score)
        == expected_module_score
    )


@pytest.mark.parametrize(
    "module_score,expected_module_score",
    [
        (100, "A"),
        (70, "A"),
        (69.8, "B"),
        (60, "B"),
        (59.6, "C"),
        (50, "C"),
        (49.8, "D"),
        (40, "D"),
        (39.7, "E/F"),
        (0, "E/F"),
    ],
)
def test_ects_equivalent(module_score, expected_module_score):
    assert (
        grades_helpers.get_ects_equivalent_score(module_score)
        == expected_module_score
    )


@pytest.mark.parametrize(
    "average,expected_gpa",
    [
        (100, 4),
        (70, 4),
        (69.9, 3.7),
        (65, 3.7),
        (64.5, 3.3),
        (60, 3.3),
        (59, 3),
        (55, 3),
        (54.6, 2.7),
        (50, 2.7),
        (49.7, 2.3),
        (45, 2.3),
        (44.8, 2),
        (40, 2),
        (39.9, 1),
        (35, 1),
        (34.8, 0),
        (0, 0),
    ],
)
def test_uk_gpa(average, expected_gpa):
    assert grades_helpers.get_uk_gpa(average) == expected_gpa


@pytest.mark.parametrize(
    "average,expected_gpa",
    [
        (100, 4),
        (70, 4),
        (69.9, 3.7),
        (65, 3.7),
        (64.5, 3.3),
        (60, 3.3),
        (59, 3),
        (55, 3),
        (54.6, 2.7),
        (50, 2.7),
        (49.7, 2.3),
        (45, 2.3),
        (44.8, 2),
        (40, 2),
        (39.9, 1),
        (35, 1),
        (34.8, 0),
        (0, 0),
    ],
)
def test_uk_gpa_in_progress(average, expected_gpa):
    assert grades_helpers.get_uk_gpa(average) == expected_gpa


@pytest.mark.parametrize(
    "average,expected_gpa",
    [
        (100, 4.0),
        (93, 4.0),
        (92, 3.7),
        (90, 3.7),
        (89, 3.3),
        (87, 3.3),
        (86, 3.0),
        (83, 3.0),
        (82, 2.7),
        (80, 2.7),
        (79, 2.3),
        (77, 2.3),
        (76, 2.0),
        (73, 2.0),
        (72, 1.7),
        (70, 1.7),
        (69, 1.3),
        (67, 1.3),
        (66, 1.0),
        (63, 1.0),
        (62, 0.7),
        (60, 0.7),
        (59, 0),
        (29, 0),
        (0, 0),
    ],
)
def test_us_gpa(average, expected_gpa):
    """Use the standard 4.0 GPA scale with pluses and minuses:
    A/A-, B+/B/B-, etc."""
    assert grades_helpers.get_us_gpa(average) == expected_gpa


@pytest.mark.parametrize(
    "average,expected_gpa",
    [
        (100, 4.0),
        (93, 4.0),
        (92, 3.7),
        (90, 3.7),
        (89, 3.3),
        (87, 3.3),
        (86, 3.0),
        (83, 3.0),
        (82, 2.7),
        (80, 2.7),
        (79, 2.3),
        (77, 2.3),
        (76, 2.0),
        (73, 2.0),
        (72, 1.7),
        (70, 1.7),
        (69, 1.3),
        (67, 1.3),
        (66, 1.0),
        (63, 1.0),
        (62, 0.7),
        (60, 0.7),
        (59, 0),
        (29, 0),
        (0, 0),
    ],
)
def test_us_gpa_in_progress(average, expected_gpa):
    """Use the standard 4.0 GPA scale with pluses and minuses:
    A/A-, B+/B/B-, etc."""
    assert grades_helpers.get_us_gpa(average) == expected_gpa


@pytest.mark.parametrize(
    "average,expected_class",
    [
        (100, "First Class Honours"),
        (70, "First Class Honours"),
        (71, "First Class Honours"),
        (69.9, "Second Class Honours [Upper Division]"),
        (69, "Second Class Honours [Upper Division]"),
        (60, "Second Class Honours [Upper Division]"),
        (59.9, "Second Class Honours [Lower Division]"),
        (50, "Second Class Honours [Lower Division]"),
        (49.9, "Third Class Honours"),
        (40, "Third Class Honours"),
        (39.9, "Fail"),
        (39, "Fail"),
        (0, "Fail"),
    ],
)
def test_classification(average, expected_class):
    assert grades_helpers.get_classification(average) == expected_class


def test_get_grades_as_list_of_dicts():
    expected_list = [
        {"module_name": "Module 1", "module_score": 100, "level": 4},
        {"module_name": "Module 2", "module_score": -1, "level": 4},
        {"module_name": "Module 3", "module_score": 80, "level": 4},
        {"module_name": "Module 4", "module_score": 75.5, "level": 5},
        {"module_name": "Module 5", "module_score": 0, "level": 4},
    ]
    grades = [
        {"Module 1": {"module_score": 100, "level": 4}},
        {"Module 2": {"module_score": -1, "level": 4}},
        {"Module 3": {"module_score": 80, "level": 4}},
        {"Module 4": {"module_score": 75.5, "level": 5}},
        {"Module 5": {"module_score": 0, "level": 4}},
    ]
    assert (
        grades_helpers.get_grades_list_as_list_of_dicts(grades)
        == expected_list
    )
