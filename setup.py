import pathlib
from setuptools import find_packages, setup
from uol_grades_calculator import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="uol-grades-calculator",
    version=__version__,
    description="Grades calculator for the BSc Computer Science at the University of London",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sglavoie/uol-grades-calculator",
    author="Sébastien Lavoie",
    author_email="sebastien@lavoie.dev",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["PyYAML", "Click"],
    entry_points={
        "console_scripts": [
            "ugc=uol_grades_calculator.cli:cli",
        ]
    },
)
