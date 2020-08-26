"""
Test suite for `grades_calculator`.
"""
# Standard library imports
import json
import uuid
from unittest.mock import patch

# Third-party library imports
import pytest


class TestGradesAreLoadedProperly:
    @staticmethod
    def test_grades_json_is_loaded_as_dict(grades):
        grades.load()
        assert isinstance(grades.grades, dict)

    @staticmethod
    def test_no_grades_json_raises_file_not_found(grades):
        with pytest.raises(FileNotFoundError):
            non_existent_file = str(uuid.uuid4()) + ".json"
            grades.load(grades_file=non_existent_file)


class TestJsonStructureIsFormattedWell:
    @staticmethod
    def test_garbage_json_file_raises_error(grades):
        with pytest.raises(json.decoder.JSONDecodeError):
            grades.load(grades_file="tests/fixtures/json/bad_format.json")

    @staticmethod
    @pytest.mark.parametrize(
        "score,expected_bool",
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
    def test_grades_scores_are_valid(grades, score, expected_bool):
        assert grades.score_is_valid(score) == expected_bool


class TestDataIsRetrievedCorrectly:
    @staticmethod
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
    def test_weight_level_of_module(grades, level, expected_weight):
        """Check that the correct weight is given to each level.
        Level 4 should return 1.
        Level 5 should return 3.
        Level 6 should return 5.
        Anything else should return 0.
        """
        assert grades.get_weight_of(level) == expected_weight

    @staticmethod
    def test_count_finished_modules(grades):
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 100},
                "Module 2": {"score": 0},
                "Module 3": {"score": 80},
                "Module 4": {"score": 75.5},
                "Module 6": {"score": -1},
                "Module 5": {"level": 4},
                "Module 7": {},
            },
            clear=True,
        ):
            # All are valid except `Module 5` which doesn't have a score
            # `0` means FAILED, `-1` means we got recognition of prior learning
            assert grades.get_num_of_finished_modules() == 5

    @staticmethod
    def test_get_list_of_finished_modules(grades):
        expected_list = [
            {"Module 1": {"score": 100}},
            {"Module 2": {"score": -1}},
            {"Module 3": {"score": 80}},
            {"Module 4": {"score": 75.5}},
            {"Module 5": {"score": 0}},
        ]
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 100},
                "Module 2": {"score": -1},
                "Module 3": {"score": 80},
                "Module 4": {"score": 75.5},
                "Module 5": {"score": 0},
                "Module 6": {"level": 4},
                "Module 7": {},
            },
            clear=True,
        ):
            # `0` means the module was FAILED. `-1` means the module was
            # not taken but has been recognized through prior learning, so
            # it is also considered done.
            assert grades.get_list_of_finished_modules() == expected_list

    @staticmethod
    def test_get_scores_of_finished_modules(grades):
        expected_list = [100, 80, 75.5, 0]
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 100},
                "Module 3": {"score": 80},
                "Module 4": {"score": 75.5},
                "Module 6": {"score": 0},
                "Module 2": {"score": -1},
                "Module 5": {"level": 4},
                "Module 7": {},
            },
            clear=True,
        ):
            assert grades.get_scores_of_finished_modules() == expected_list


class TestDataIsCalculatedWell:
    @staticmethod
    def test_calculate_average_of_finished_modules_rounds_half_up(grades):
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 100},
                "Module 3": {"score": 80},
                "Module 4": {"score": 79.7},
                "Module 6": {"score": 0},
                "Module 2": {"score": -1},
                "Module 5": {"level": 4},
                "Module 5": {},
            },
            clear=True,
        ):
            assert grades.calculate_average_of_finished_modules() == 64.93
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 97.23},
                "Module 2": {"score": 93.58},
                "Module 3": {"score": 91.11},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            assert grades.calculate_average_of_finished_modules() == 93.97
        with patch.dict(
            grades.grades, {}, clear=True,
        ):
            assert grades.calculate_average_of_finished_modules() == 0

    @staticmethod
    @pytest.mark.parametrize(
        "score,expected_class",
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
    def test_classification(grades, score, expected_class, monkeypatch):
        monkeypatch.setattr(grades, "average", score, raising=True)
        assert grades.get_classification() == expected_class

    @staticmethod
    @pytest.mark.parametrize(
        "score,expected_gpa",
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
    def test_uk_gpa(grades, score, expected_gpa, monkeypatch):
        monkeypatch.setattr(grades, "average", score, raising=True)
        assert grades.get_uk_gpa() == expected_gpa

    @staticmethod
    @pytest.mark.parametrize(
        "score,expected_gpa",
        [
            (100, 4),
            (95, 3.75),
            (93, 3.65),
            (90, 3.5),
            (87, 3.35),
            (82, 3.1),
            (59, 1.95),
            (51, 1.55),
            (29, 0.45),
            (21, 0.05),
            (20, 0),
            (12, 0),
            (0, 0),
        ],
    )
    def test_us_gpa(grades, score, expected_gpa, monkeypatch):
        monkeypatch.setattr(grades, "average", score, raising=True)
        assert grades.get_us_gpa() == expected_gpa

    @staticmethod
    @pytest.mark.parametrize(
        "score,expected_score",
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
    def test_ects_equivalent(grades, score, expected_score, monkeypatch):
        monkeypatch.setattr(grades, "average", score, raising=True)
        assert grades.get_ects_equivalent_score(score) == expected_score

    @staticmethod
    def test_ects_equivalent_list_of_scores_conversion(grades):
        expected_scores = {
            "Module 1": "A",
            "Module 2": "N/A",
            "Module 3": "B",
            "Module 4": "C",
            "Module 5": "E/F",
            "Module 6": "A",
            "Module 7": "D",
        }
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": 95.2},
                "Module 2": {"score": -1},  # not counted
                "Module 3": {"score": 60},
                "Module 4": {"score": 50.3},
                "Module 5": {"score": 0},
                "Module 6": {"score": 100},
                "Module 7": {"score": 41},
            },
            clear=True,
        ):
            out = grades.get_ects_scores_of_finished_modules()
            assert out == expected_scores

    @staticmethod
    def test_get_total_credits(grades):
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": -1, "level": 4},  # counts as done
                "Module 2": {"score": 80, "level": 5},
                "Module 3": {"score": 70, "level": 6},
                "Module 4": {},  # don't count when there's no data
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 45
        with patch.dict(
            grades.grades,
            {"Final Project": {"score": 80}},  # counts double
            clear=True,
        ):
            assert grades.get_total_credits() == 30
        with patch.dict(
            grades.grades,
            {
                "final project": {
                    "score": 80
                },  # make sure capitalization does not matter
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 30
        with patch.dict(
            grades.grades,
            {
                "Module 1": {"score": -1},  # counts as done
                "Final Project": {"score": 80},  # counts double
                "Module 3": {"score": 90.5},
                "Module 4": {"level": 5},  # don't count when there's no score
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 60
        with patch.dict(
            grades.grades,
            {
                "Module 3": {"score": 90.5},
                "Module 4": {"level": 5},
                "Module 4": {"score": 34},  # do not count failed attempts
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 15

    @staticmethod
    @pytest.mark.parametrize(
        "num_credits,exp_percentage",
        [
            (0, 0),
            (15, 4.17),
            (30, 8.33),
            (60, 16.67),
            (135, 37.5),
            (240, 66.67),
            (300, 83.33),
            (360, 100),
            (375, -1),  # can't have more than 360 credits
        ],
    )
    def test_get_percentage_degree_done(
        grades, num_credits, exp_percentage, monkeypatch
    ):
        monkeypatch.setattr(grades, "total_credits", num_credits, raising=True)
        assert grades.get_percentage_degree_done() == exp_percentage
