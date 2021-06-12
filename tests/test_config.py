"""
Test config.py
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import pytest

# Local imports
from ugc.config import Config
from ugc.errors import ConfigValidationError


def test_self_path_is_set_to_custom_path():
    custom_path = "/home/user/custom.yml"
    config = Config(config_path=custom_path)
    assert config.path == custom_path


def test_self_path_is_set_to_default_path():
    default_path = f"{str(Path.home())}/.grades.yml"  # should mock...
    assert Config().path == default_path


def test_grades_yml_is_loaded_as_dict(local_config):
    data = local_config.load()
    assert isinstance(data, dict)


def test_bad_format_grades_yml_raises_ConfigValidationError(local_bad_config):
    with pytest.raises(ConfigValidationError):
        local_bad_config.load()


def test_config_file_exists_but_is_empty_raises_ConfigValidationError(
    local_config,
):
    local_config.path = Path(__file__).parent / "fixtures/yaml/empty.yml"
    with pytest.raises(ConfigValidationError):
        local_config.load()


@pytest.mark.parametrize(
    "final_weight,midterm_weight,expected_value",
    [
        (40, 60, True),  # weight = 100
        (None, None, True),  # missing all values is OK
    ],
)
def test_check_total_weight_sums_up_100(
    local_config, final_weight, midterm_weight, expected_value
):
    module = {
        "final_weight": final_weight,
        "midterm_weight": midterm_weight,
    }
    assert (
        local_config._check_total_weight_sums_up_100_for_module(module, "name")
        == expected_value
    )


@pytest.mark.parametrize(
    "final_weight,midterm_weight",
    [
        (30, 60),  # weight < 100
        (50, 60),  # weight > 100
        (40.4, 60),  # final_weight not an int
        (40, 60.4),  # midterm_weight not an int
        (39.5, 60.5),  # weights not int
        (None, 60),  # final_weight missing
        (40, None),  # midterm_weight missing
    ],
)
def test_check_total_weight_sums_up_100_raises_error(
    local_config, final_weight, midterm_weight
):
    with pytest.raises(ConfigValidationError):
        module = {
            "final_weight": final_weight,
            "midterm_weight": midterm_weight,
        }
        assert local_config._check_total_weight_sums_up_100_for_module(
            module, "module_name"
        )


def test_check_total_weight_sums_up_100_all_modules_raises_error(local_config):
    with pytest.raises(ConfigValidationError):
        config_false = {
            "module1": {"final_weight": 40, "midterm_weight": 60},  # OK
            "module2": {"final_weight": 30, "midterm_weight": 60},  # not 100
        }
        local_config.data = config_false
        assert local_config.check_total_weight_sums_up_100_in_all_modules()


def test_check_total_weight_sums_up_100_all_modules(local_config):
    config_true_1 = {
        "module1": {},  # missing both values is OK
    }
    local_config.data = config_true_1
    assert local_config.check_total_weight_sums_up_100_in_all_modules()

    config_true_2 = {
        "module1": {"final_weight": 40, "midterm_weight": 60},
        "module2": {"final_weight": 50, "midterm_weight": 50},
    }
    local_config.data = config_true_2
    assert local_config.check_total_weight_sums_up_100_in_all_modules()


def test_check_score_accuracy_raises_error_on_RPLed_module_with_scores(
    local_config,
):
    with pytest.raises(ConfigValidationError):
        local_config.data["How Computers Work"] = {
            "final_score": 50,  # Should be None
            "final_weight": 50,
            "midterm_score": 50,  # Should be None
            "midterm_weight": 50,
            "module_score": -1,
        }
        local_config.check_score_accuracy_raises_error_on_RPLed_module_with_scores()


def test_all_modules_are_found_with_valid_names_returns_True(local_config):
    local_config.data = local_config.default.copy()
    assert local_config.all_modules_are_found_with_valid_names()


def test_all_modules_are_found_with_missing_modules_raises_ConfigValidationError(
    local_config,
):
    with pytest.raises(ConfigValidationError):
        local_config.default.pop("Final Project")  # missing one module
        # print(config_false_1)
        local_config.all_modules_are_found_with_valid_names()


def test_all_modules_are_found_with_extra_modules_raises_ConfigValidationError(
    local_config,
):
    with pytest.raises(ConfigValidationError):
        local_config.data = local_config.default.copy()
        local_config.data["Module 24"] = {}  # nonexistent module
        local_config.all_modules_are_found_with_valid_names()


def test_all_modules_are_set_to_correct_level_returns_True(local_config):
    local_config.data = local_config.default.copy()
    assert local_config.all_modules_are_set_to_correct_level()


def test_all_modules_are_set_to_correct_level_raises_ConfigValidationError_on_missing(
    local_config,
):
    with pytest.raises(ConfigValidationError):
        local_config.data = local_config.default.copy()
        local_config.data["Discrete Mathematics"] = None
        local_config.all_modules_are_set_to_correct_level()
