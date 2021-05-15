import pathlib
import os
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open(
    os.path.join(HERE, "uol_grades_calculator", "__version__.py")
) as fp:
    about = {}
    exec(fp.read(), about)

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="uol-grades-calculator",
    version=about["__version__"],
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
