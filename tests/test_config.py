"""
Test config.py
"""

# Standard library imports
from pathlib import Path

# Local imports
from uol_grades_calculator.config import Config


class TestConfigIsLoadedProperly:
    @staticmethod
    def test_self_path_is_set_to_custom_path():
        custom_path = "/home/user/custom.yml"
        config = Config(config_path=custom_path)
        assert config.path == custom_path

    @staticmethod
    def test_self_path_is_set_to_default_path():
        default_path = f"{str(Path.home())}/.grades.yml"  # should mock...
        assert Config().path == default_path

    @staticmethod
    def test_grades_yml_is_loaded_as_dict(local_config):
        data = local_config.load()
        assert isinstance(data, dict)
