"""
Test config.py
"""

# Standard library imports
from pathlib import Path

# Third-party library imports
import pytest

# Local imports
from uol_grades_calculator.config import Config
from uol_grades_calculator.errors import ConfigValidationError


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
        local_config.check_total_weight_sums_up_100_for_module(module, "name")
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
        assert local_config.check_total_weight_sums_up_100_for_module(
            module, "module_name"
        )


def test_check_total_weight_sums_up_100_all_modules_raises_error(local_config):
    with pytest.raises(ConfigValidationError):
        config_false = {
            "module1": {"final_weight": 40, "midterm_weight": 60},  # OK
            "module2": {"final_weight": 30, "midterm_weight": 60},  # not 100
        }
        local_config.config = config_false
        assert local_config.check_total_weight_sums_up_100_in_all_modules()


def test_check_total_weight_sums_up_100_all_modules(local_config):
    config_true_1 = {
        "module1": {},  # missing both values is OK
    }
    local_config.config = config_true_1
    assert local_config.check_total_weight_sums_up_100_in_all_modules()

    config_true_2 = {
        "module1": {"final_weight": 40, "midterm_weight": 60},
        "module2": {"final_weight": 50, "midterm_weight": 50},
    }
    local_config.config = config_true_2
    assert local_config.check_total_weight_sums_up_100_in_all_modules()
