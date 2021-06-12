"""
Test grades.py
"""
# Standard library imports
from unittest.mock import patch

# Third-party library imports
import pytest


class TestDataIsRetrievedCorrectly:
    @staticmethod
    def test_count_finished_modules(local_grades):
        with patch.dict(
            local_grades.data,
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
            assert local_grades.get_num_of_finished_modules() == 5

    @staticmethod
    def test_get_list_of_finished_modules(local_grades):
        expected_list = [
            {"Module 1": {"module_score": 100, "level": 4}},
            {"Module 2": {"module_score": -1, "level": 4}},
            {"Module 3": {"module_score": 80, "level": 4}},
            {"Module 4": {"module_score": 75.5, "level": 5}},
            {"Module 5": {"module_score": 0, "level": 4}},
        ]
        with patch.dict(
            local_grades.data,
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
            assert local_grades.get_list_of_finished_modules() == expected_list

    @staticmethod
    def test_get_list_of_modules_in_progress(local_grades):
        local_grades.data["Algorithms and Data Structures I"] = {
            "final_score": 65,
            "final_weight": 70,
            "midterm_score": 79,
            "midterm_weight": 30,
            "module_score": None,
            "level": 4,
        }
        local_grades.data["Agile Software Projects"] = {
            "final_score": None,
            "final_weight": 70,
            "midterm_score": 60,
            "midterm_weight": 30,
            "module_score": None,
            "level": 5,
        }
        local_grades.data["Algorithms and Data Structures II"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 75,
            "midterm_weight": 50,
            "module_score": None,
            "level": 5,
        }

        expected_list = [
            {
                "Algorithms and Data Structures I": {
                    "final_score": 65,
                    "final_weight": 70,
                    "midterm_score": 79,
                    "midterm_weight": 30,
                    "level": 4,
                }
            },
            {
                "Agile Software Projects": {
                    "midterm_score": 60,
                    "midterm_weight": 30,
                    "level": 5,
                }
            },
            {
                "Algorithms and Data Structures II": {
                    "midterm_score": 75,
                    "midterm_weight": 50,
                    "level": 5,
                }
            },
        ]
        assert local_grades.get_list_of_modules_in_progress() == expected_list

    @staticmethod
    def test_get_scores_of_modules_in_progress(local_grades):
        local_grades.data["Algorithms and Data Structures I"] = {
            "final_score": 65,
            "final_weight": 70,
            "midterm_score": 79,
            "midterm_weight": 30,
            "module_score": None,
            "level": 4,
        }
        local_grades.data["Agile Software Projects"] = {
            "final_score": None,
            "final_weight": 70,
            "midterm_score": 60,
            "midterm_weight": 30,
            "module_score": None,
            "level": 5,
        }
        local_grades.data["Algorithms and Data Structures II"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 75,
            "midterm_weight": 50,
            "module_score": None,
            "level": 5,
        }
        results = (
            local_grades.get_scores_of_modules_in_progress()
        )
        assert results == [69.2, 60, 75]

    @staticmethod
    def test_get_module_scores_of_finished_modules(local_grades):
        expected_list = [100, 80, 75.5, 0]
        with patch.dict(
            local_grades.data,
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
                local_grades.get_module_scores_of_finished_modules()
                == expected_list
            )


class TestDataIsCalculatedWell:
    @staticmethod
    def test_calculate_unweighted_average(local_grades):
        with patch.dict(
            local_grades.data,
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
            assert local_grades.calculate_unweighted_average() == 86.57
        with patch.dict(
            local_grades.data,
            {
                "Module 1": {"module_score": 97.23, "level": 4},
                "Module 2": {"module_score": 93.58, "level": 4},
                "Module 3": {"module_score": 91.11, "level": 4},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            assert local_grades.calculate_unweighted_average() == 93.97
        with patch.dict(
            local_grades.data,
            {},
            clear=True,
        ):
            assert local_grades.calculate_unweighted_average() == 0

    @staticmethod
    def test_calculate_weighted_average(
        local_grades,
    ):
        with patch.dict(
            local_grades.data,
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
            assert local_grades.calculate_weighted_average() == 84.78
        with patch.dict(
            local_grades.data,
            {
                "Module 1": {"module_score": 97.23, "level": 4},
                "Module 2": {"module_score": 93.58, "level": 5},
                "Module 3": {"module_score": 91.11, "level": 6},
                "Module 4": {},
                "Module 5": {"level": 4},
            },
            clear=True,
        ):
            assert local_grades.calculate_weighted_average() == 92.61
        with patch.dict(
            local_grades.data,
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
            assert local_grades.calculate_weighted_average() == 90.57
        with patch.dict(
            local_grades.data,
            {},
            clear=True,
        ):
            assert local_grades.calculate_weighted_average() == 0

    @staticmethod
    def test_calculate_unweighted_average_in_progress(
        local_grades,
    ):
        # in progress: [69.2, 60, 75]
        local_grades.data["Algorithms and Data Structures I"] = {
            "final_score": 65,
            "final_weight": 70,
            "midterm_score": 79,
            "midterm_weight": 30,
            "module_score": None,
            "level": 4,
        }
        local_grades.data["Agile Software Projects"] = {
            "final_score": None,
            "final_weight": 70,
            "midterm_score": 60,
            "midterm_weight": 30,
            "module_score": None,
            "level": 5,
        }
        local_grades.data["Algorithms and Data Structures II"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 75,
            "midterm_weight": 50,
            "module_score": None,
            "level": 5,
        }

        # finished : [80, 82, 85]
        local_grades.data["How Computers Work"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 60,
            "midterm_weight": 50,
            "module_score": 80,
            "level": 4,
        }
        local_grades.data["Introduction to Programming I"] = {
            "final_score": 80,
            "final_weight": 50,
            "midterm_score": 60,
            "midterm_weight": 50,
            "module_score": 82,
            "level": 4,
        }
        local_grades.data["Computational Mathematics"] = {
            "final_score": 80,
            "final_weight": 50,
            "midterm_score": None,
            "midterm_weight": 50,
            "module_score": 85,
            "level": 4,
        }

        # average of all that: 75.67
        result = (
            local_grades.calculate_unweighted_average_in_progress()
        )
        assert result == 75.2

    @staticmethod
    def test_calculate_weighted_average_in_progress(
        local_grades,
    ):
        # in progress: [69.2, 60, 75], respectively [L4, L5, L5]
        local_grades.data["Algorithms and Data Structures I"] = {
            "final_score": 65,
            "final_weight": 70,
            "midterm_score": 79,
            "midterm_weight": 30,
            "module_score": None,
            "level": 4,
        }
        local_grades.data["Agile Software Projects"] = {
            "final_score": None,
            "final_weight": 70,
            "midterm_score": 60,
            "midterm_weight": 30,
            "module_score": None,
            "level": 5,
        }
        local_grades.data["Algorithms and Data Structures II"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 75,
            "midterm_weight": 50,
            "module_score": None,
            "level": 5,
        }

        # finished : [80, 82, 85], respectively [L4, L4, L4]
        local_grades.data["How Computers Work"] = {
            "final_score": None,
            "final_weight": 50,
            "midterm_score": 60,
            "midterm_weight": 50,
            "module_score": 80,
            "level": 4,
        }
        local_grades.data["Introduction to Programming I"] = {
            "final_score": 80,
            "final_weight": 50,
            "midterm_score": 60,
            "midterm_weight": 50,
            "module_score": 82,
            "level": 4,
        }
        local_grades.data["Computational Mathematics"] = {
            "final_score": 80,
            "final_weight": 50,
            "midterm_score": None,
            "midterm_weight": 50,
            "module_score": 85,
            "level": 4,
        }

        # weighted average of all that: 72.12
        result = (
            local_grades.calculate_weighted_average_in_progress()
        )
        assert result == 72.12

    @staticmethod
    def test_get_module_scores_of_finished_modules_for_system_us(local_grades):
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
            local_grades.data,
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
            out = (
                local_grades.get_module_scores_of_finished_modules_for_system(
                    system="US"
                )
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_scores_of_modules_in_progress_for_system_us(local_grades):
        expected_module_scores = {
            "Module 1": "A",
            "Module 3": "B",
            "Module 4": "C",
        }
        with patch.dict(
            local_grades.data,
            {
                "Module 1": {
                    "final_score": 95.2,
                    "final_weight": 70,
                    "level": 4,
                },
                "Module 2": {
                    "module_score": -1,
                    "level": 4,
                },  # not counted: i.e. N/A
                "Module 3": {
                    "midterm_score": 85.5,
                    "midterm_weight": 50,
                    "level": 4,
                },
                "Module 4": {
                    "final_score": 70,
                    "final_weight": 70,
                    "midterm_score": 80,
                    "midterm_weight": 30,
                    "level": 4,
                },
                "Module 5": {
                    "module_score": 59.2,
                    "level": 4,
                },  # not counted: module_score is present
                "Module 6": {
                    "module_score": 59.2,
                    "final_score": 59.2,
                    "final_weight": 70,
                    "midterm_score": 59.2,
                    "midterm_weight": 30,
                    "level": 4,
                },  # not counted: module_score is present
            },
            clear=True,
        ):
            out = local_grades.get_scores_of_modules_in_progress_for_system(
                system="US"
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_scores_of_modules_in_progress_for_system_ects(
        local_grades,
    ):
        expected_module_scores = {
            "Module 1": "A",
            "Module 3": "A",
            "Module 4": "C",
        }
        with patch.dict(
            local_grades.data,
            {
                "Module 1": {
                    "final_score": 95.2,
                    "final_weight": 70,
                    "level": 4,
                },
                "Module 2": {
                    "module_score": -1,
                    "level": 4,
                },  # not counted: i.e. N/A
                "Module 3": {
                    "midterm_score": 85.5,
                    "midterm_weight": 50,
                    "level": 4,
                },
                "Module 4": {
                    "final_score": 55,
                    "final_weight": 70,
                    "midterm_score": 54,
                    "midterm_weight": 30,
                    "level": 4,
                },
                "Module 5": {
                    "module_score": 59.2,
                    "level": 4,
                },  # not counted: module_score is present
                "Module 6": {
                    "module_score": 59.2,
                    "final_score": 59.2,
                    "final_weight": 70,
                    "midterm_score": 59.2,
                    "midterm_weight": 30,
                    "level": 4,
                },  # not counted: module_score is present
            },
            clear=True,
        ):
            out = local_grades.get_scores_of_modules_in_progress_for_system(
                system="ECTS"
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_module_scores_of_finished_modules_for_system_ects(
        local_grades,
    ):
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
            local_grades.data,
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
            out = (
                local_grades.get_module_scores_of_finished_modules_for_system(
                    system="ECTS"
                )
            )
            assert out == expected_module_scores

    @staticmethod
    def test_get_total_credits(local_grades):
        with patch.dict(
            local_grades.data,
            {
                "Module 1": {"module_score": -1, "level": 4},  # counts as done
                "Module 2": {"module_score": 80, "level": 5},
                "Module 3": {"module_score": 70, "level": 6},
                "Module 4": {},  # don't count when there's no data
            },
            clear=True,
        ):
            assert local_grades.get_total_credits() == 45
        with patch.dict(
            local_grades.data,
            {
                "Final Project": {"module_score": 80, "level": 6}
            },  # counts double
            clear=True,
        ):
            assert local_grades.get_total_credits() == 30
        with patch.dict(
            local_grades.data,
            {
                "final project": {
                    "module_score": 80,
                    "level": 6,
                },  # make sure capitalization does not matter
            },
            clear=True,
        ):
            assert local_grades.get_total_credits() == 30
        with patch.dict(
            local_grades.data,
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
            assert local_grades.get_total_credits() == 60
        with patch.dict(
            local_grades.data,
            {
                # do not count failed attempts
                "Module 2": {"module_score": 34, "level": 4},
                "Module 3": {"module_score": 90.5, "level": 4},
                "Module 4": {"level": 4},
            },
            clear=True,
        ):
            assert local_grades.get_total_credits() == 15

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
        local_grades, num_credits, exp_percentage, monkeypatch
    ):
        monkeypatch.setattr(
            local_grades, "total_credits", num_credits, raising=True
        )
        assert local_grades.get_percentage_degree_done() == exp_percentage
