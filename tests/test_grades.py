"""
Test suite for `grades_calculator`.
"""
# Standard library imports
from unittest.mock import patch

# Third-party library imports
import pytest


class TestGradesAreLoadedProperly:
    @staticmethod
    def test_grades_yml_is_loaded_as_dict(grades):
        grades.load()
        assert isinstance(grades.data, dict)


class TestYMLStructureIsFormattedWell:
    @staticmethod
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
    def test_grades_module_scores_are_valid(
        grades, module_score, expected_bool
    ):
        assert grades.module_score_is_valid(module_score) == expected_bool


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
            grades.data,
            {
                "Module 1": {"module_score": 100, "level": 4},
                "Module 2": {"module_score": 0, "level": 4},
                "Module 3": {"module_score": 80, "level": 4},
                "Module 4": {"module_score": 75.5, "level": 4},
                "Module 6": {"module_score": -1, "level": 4},
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
            {"Module 1": {"module_score": 100, "level": 4}},
            {"Module 2": {"module_score": -1, "level": 4}},
            {"Module 3": {"module_score": 80, "level": 4}},
            {"Module 4": {"module_score": 75.5, "level": 5}},
            {"Module 5": {"module_score": 0, "level": 4}},
        ]
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 100, "level": 4},
                "Module 2": {"module_score": -1, "level": 4},
                "Module 3": {"module_score": 80, "level": 4},
                "Module 4": {"module_score": 75.5, "level": 5},
                "Module 5": {"module_score": 0, "level": 4},
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
    def test_get_module_scores_of_finished_modules(grades):
        expected_list = [100, 80, 75.5, 0]
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 100, "level": 4},
                "Module 3": {"module_score": 80, "level": 4},
                "Module 4": {"module_score": 75.5, "level": 4},
                "Module 6": {"module_score": 0, "level": 4},
                "Module 2": {"module_score": -1},
                "Module 5": {"level": 4},
                "Module 7": {},
            },
            clear=True,
        ):
            assert (
                grades.get_module_scores_of_finished_modules() == expected_list
            )


class TestDataIsCalculatedWell:
    @staticmethod
    def test_calculate_unweighted_average(grades):
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 100, "level": 4},
                "Module 2": {"module_score": -1, "level": 5},
                "Module 3": {"module_score": 80, "level": 6},
                "Module 4": {"module_score": 79.7, "level": 4},
                "Module 5": {"level": 4},
                "Module 6": {"module_score": 0},
                "Module 7": {},
            },
            clear=True,
        ):
            assert grades.calculate_unweighted_average() == 86.57
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 97.23, "level": 4},
                "Module 2": {"module_score": 93.58, "level": 4},
                "Module 3": {"module_score": 91.11, "level": 4},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            assert grades.calculate_unweighted_average() == 93.97
        with patch.dict(
            grades.data,
            {},
            clear=True,
        ):
            assert grades.calculate_unweighted_average() == 0

    @staticmethod
    def test_calculate_weighted_average(
        grades,
    ):
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 100, "level": 4},
                "Module 2": {"module_score": -1, "level": 4},
                "Module 3": {"module_score": 80},
                "Module 4": {"module_score": 79.7, "level": 5},
                "Module 5": {"level": 4},
                "Module 6": {"module_score": 0},
                "Module 7": {},
            },
            clear=True,
        ):
            # skip module 3: `level` is expected
            assert grades.calculate_weighted_average() == 84.78
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 97.23, "level": 4},
                "Module 2": {"module_score": 93.58, "level": 5},
                "Module 3": {"module_score": 91.11, "level": 6},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            assert grades.calculate_weighted_average() == 92.61
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 97.23, "level": 4},
                "Module 2": {"module_score": 93.58, "level": 5},
                "Final Project": {"module_score": 89, "level": 6},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            # weight of "Final Project" is twice that of another module level 6
            # (97.23 + 93.58 * 3 + 89 * 10) / 14
            assert grades.calculate_weighted_average() == 90.57
        with patch.dict(
            grades.data,
            {},
            clear=True,
        ):
            assert grades.calculate_weighted_average() == 0

    @staticmethod
    @pytest.mark.parametrize(
        "module_score,expected_class",
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
    def test_classification(grades, module_score, expected_class, monkeypatch):
        monkeypatch.setattr(
            grades, "weighted_average", module_score, raising=True
        )
        assert grades.get_classification() == expected_class

    @staticmethod
    @pytest.mark.parametrize(
        "module_score,expected_gpa",
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
    def test_uk_gpa(grades, module_score, expected_gpa, monkeypatch):
        monkeypatch.setattr(
            grades, "weighted_average", module_score, raising=True
        )
        assert grades.get_uk_gpa() == expected_gpa

    @staticmethod
    @pytest.mark.parametrize(
        "module_score,expected_gpa",
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
    def test_us_gpa(grades, module_score, expected_gpa, monkeypatch):
        """Use the standard 4.0 GPA scale with pluses and minuses:
        A/A-, B+/B/B-, etc."""
        monkeypatch.setattr(
            grades, "weighted_average", module_score, raising=True
        )
        assert grades.get_us_gpa() == expected_gpa

    @staticmethod
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
    def test_ects_equivalent(
        grades, module_score, expected_module_score, monkeypatch
    ):
        monkeypatch.setattr(
            grades, "weighted_average", module_score, raising=True
        )
        assert (
            grades.get_ects_equivalent_score(module_score)
            == expected_module_score
        )

    @staticmethod
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
    def test_us_letter_equivalent_score(
        grades, module_score, expected_module_score, monkeypatch
    ):
        monkeypatch.setattr(
            grades, "weighted_average", module_score, raising=True
        )
        assert (
            grades.get_us_letter_equivalent_score(module_score)
            == expected_module_score
        )

    @staticmethod
    def test_get_module_scores_of_finished_modules_for_system_us(grades):
        expected_module_scores = {
            "Module 1": "A",
            "Module 2": "N/A",
            "Module 3": "B",
            "Module 4": "C",
            "Module 5": "F",
            "Module 6": "A",
            "Module 7": "D",
            "Module 8": "A-",
            "Module 9": "B+",
            "Module 10": "B-",
            "Module 11": "C+",
            "Module 12": "C-",
            "Module 13": "D+",
            "Module 14": "D-",
        }
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 95.2, "level": 4},
                "Module 2": {
                    "module_score": -1,
                    "level": 4,
                },  # not counted: i.e. N/A
                "Module 3": {"module_score": 85, "level": 4},
                "Module 4": {"module_score": 74.2, "level": 4},
                "Module 5": {"module_score": 59.2, "level": 4},
                "Module 6": {"module_score": 100, "level": 4},
                "Module 7": {"module_score": 64.5, "level": 4},
                "Module 8": {"module_score": 91, "level": 4},
                "Module 9": {"module_score": 88.7, "level": 5},
                "Module 10": {"module_score": 81.4, "level": 5},
                "Module 11": {"module_score": 79, "level": 5},
                "Module 12": {"module_score": 70, "level": 5},
                "Module 13": {"module_score": 67.1, "level": 5},
                "Module 14": {"module_score": 61, "level": 5},
            },
            clear=True,
        ):
            out = grades.get_module_scores_of_finished_modules_for_system(
                system="US"
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_module_scores_of_finished_modules_for_system_ects(grades):
        expected_module_scores = {
            "Module 1": "A",
            "Module 2": "N/A",
            "Module 3": "B",
            "Module 4": "C",
            "Module 5": "E/F",
            "Module 6": "A",
            "Module 7": "D",
        }
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": 95.2, "level": 4},
                "Module 2": {"module_score": -1, "level": 4},  # not counted
                "Module 3": {"module_score": 60, "level": 4},
                "Module 4": {"module_score": 50.3, "level": 4},
                "Module 5": {"module_score": 0, "level": 4},
                "Module 6": {"module_score": 100, "level": 4},
                "Module 7": {"module_score": 41, "level": 4},
            },
            clear=True,
        ):
            out = grades.get_module_scores_of_finished_modules_for_system(
                system="ECTS"
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_total_credits(grades):
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": -1, "level": 4},  # counts as done
                "Module 2": {"module_score": 80, "level": 5},
                "Module 3": {"module_score": 70, "level": 6},
                "Module 4": {},  # don't count when there's no data
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 45
        with patch.dict(
            grades.data,
            {
                "Final Project": {"module_score": 80, "level": 6}
            },  # counts double
            clear=True,
        ):
            assert grades.get_total_credits() == 30
        with patch.dict(
            grades.data,
            {
                "final project": {
                    "module_score": 80,
                    "level": 6,
                },  # make sure capitalization does not matter
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 30
        with patch.dict(
            grades.data,
            {
                "Module 1": {"module_score": -1, "level": 5},  # counts as done
                "Final Project": {
                    "module_score": 80,
                    "level": 6,
                },  # counts double
                "Module 3": {"module_score": 90.5, "level": 5},
                "Module 4": {
                    "level": 5
                },  # don't count when there's no module_score
            },
            clear=True,
        ):
            assert grades.get_total_credits() == 60
        with patch.dict(
            grades.data,
            {
                # do not count failed attempts
                "Module 2": {"module_score": 34, "level": 4},
                "Module 3": {"module_score": 90.5, "level": 4},
                "Module 4": {"level": 5, "level": 4},
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
