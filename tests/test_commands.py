"""
Test commands.py
"""

# Standard library imports
import os

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
