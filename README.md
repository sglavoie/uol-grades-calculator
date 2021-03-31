# Grades Calculator

[![PyPi](https://img.shields.io/pypi/v/uol-grades-calculator.svg)](https://pypi.python.org/pypi/uol-grades-calculator)

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

---

### Table of contents

- [Requirements](#requirements)
- [To run the utility](#to-run-the-utility)
- [Generate a sample config file to get started](#generate-a-sample-config-file-to-get-started)
  - [Specifying a different path for the config file](#specifying-a-different-path-for-the-config-file)
- [How to fill the config file (`.grades.yml` by default)](#how-to-fill-the-config-file-gradesyml-by-default)
  - [Module taken](#module-taken)
  - [Module recognized (RPL)](#module-recognized-rpl)
- [Sample command outputs](#sample-command-outputs)
  - [`summarize`](#summarize)
- [For developers](#for-developers)
  - [To run the test suite](#to-run-the-test-suite)
  - [To develop locally as a package](#to-develop-locally-as-a-package)
  - [To publish to PyPI](#to-publish-to-pypi)

---

## Requirements

Python 3.6 and above. Install additional dependencies with the following command:

    pip install -r requirements.txt

## To run the utility

    python -m uol_grades_calculator

By passing no arguments, this will print the default help message.

## Generate a sample config file to get started

To generate a sample configuration file, run the following command:

    python -m uol_grades_calculator generate-sample

The configuration file will be created in your home directory as a hidden file (i.e. `~/.grades.yml`).

### Specifying a different path for the config file

If you want to create it somewhere else:

    python -m uol_grades_calculator --config /path/to/config/file.yml generate-sample

Note that you will have to indicate where the config is each time you use this tool in this case (you can always create an alias to avoid the trouble of typing it every time). For example:

    python -m uol_grades_calculator --config /path/to/config/file.yml summarize

## How to fill the config file (`.grades.yml` by default)

Each module described in the config file should contain information adhering to the following indications:

| YAML node         | Value                                               | Example(s)             | Optional \* |
| ----------------- | --------------------------------------------------- | ---------------------- | ----------- |
| `completion_date` | Date as a **string**: `YYYY-MM`                     | `2020-01`              | Yes         |
| `final_score`     | **Float**: _range_ 0.00–100.00                      | `50`, `50.5`, `90.56`  | Yes         |
| `final_weight`    | **Integer** expressing a percentage: _range_ 0–100  | `0`, `40`, `80`, `100` | Yes         |
| `midterm_score`   | **Float**: _range_ 0.00–100.00                      | `50`, `50.5`, `90.56`  | Yes         |
| `midterm_weight`  | **Integer** expressing a percentage: _range_ 0–100  | `0`, `40`, `80`, `100` | Yes         |
| `module_score`    | **Float**: _range_ 0.00–100.00                      | `50`, `50.5`, `90.56`  | **No**      |
| `level`           | **Integer**: choose _strictly_ from `4`, `5` or `6` | `4`, `5`, `6`          | **No**      |

\* If a node value is left empty (or the node is absent in a given module), this will affect how the module is taken into account (average across all modules, summary of modules taken, etc.).

Here is a complete example for one module:

```yaml
Algorithms and Data Structures I:
  completion_date: 2020-03
  final_score: 92
  final_weight: 50
  midterm_score: 98
  midterm_weight: 50
  module_score: 95
  level: 4
```

### Module taken

This means we define a module score between `0` and `100`, both being inclusive values.

```yaml
Algorithms and Data Structures I:
  module_score: 80.5
```

### Module recognized (RPL)

In this case, we define a score of `-1` to indicate that this module is done but we didn't get a score for it.

```yaml
Algorithms and Data Structures I:
  module_score: -1
```

## Sample command outputs

### `summarize`

    Modules taken:
    [ { 'Algorithms and Data Structures I': { 'completion_date': '2020-03',
                                              'final_score': 92,
                                              'final_weight': 50,
                                              'level': 4,
                                              'midterm_score': 98,
                                              'midterm_weight': 50,
                                              'module_score': 95}},
      { 'Discrete Mathematics': { 'completion_date': '2020-03',
                                  'final_score': 100,
                                  'final_weight': 50,
                                  'level': 4,
                                  'midterm_score': 99,
                                  'midterm_weight': 50,
                                  'module_score': 100}},
      { 'Fundamentals of Computer Science': { 'completion_date': '2020-09',
                                              'final_score': 98,
                                              'final_weight': 50,
                                              'level': 4,
                                              'midterm_score': 98,
                                              'midterm_weight': 50,
                                              'module_score': 98}},
      { 'How Computers Work': { 'completion_date': '2018-12',
                                'level': 4,
                                'module_score': -1}},
      { 'Introduction to Programming I': { 'completion_date': '2019-09',
                                          'final_score': 100,
                                          'final_weight': 50,
                                          'level': 4,
                                          'midterm_score': 100,
                                          'midterm_weight': 50,
                                          'module_score': 100}},
      { 'Numerical Mathematics': { 'completion_date': '2019-09',
                                  'final_score': 61,
                                  'final_weight': 50,
                                  'level': 4,
                                  'midterm_score': 99,
                                  'midterm_weight': 50,
                                  'module_score': 80}},
      { 'Introduction to Programming II': { 'completion_date': '2020-03',
                                            'final_score': 98,
                                            'final_weight': 70,
                                            'level': 4,
                                            'midterm_score': 100,
                                            'midterm_weight': 30,
                                            'module_score': 99}},
      { 'Web Development': { 'completion_date': '2019-09',
                            'final_score': 87,
                            'final_weight': 70,
                            'level': 4,
                            'midterm_score': 86,
                            'midterm_weight': 30,
                            'module_score': 87}},
      { 'Algorithms and Data Structures II': { 'completion_date': '2020-09',
                                              'final_score': 92,
                                              'final_weight': 50,
                                              'level': 5,
                                              'midterm_score': 92,
                                              'midterm_weight': 50,
                                              'module_score': 92}},
      { 'Object Oriented Programming': { 'completion_date': '2020-09',
                                        'final_score': 96,
                                        'final_weight': 50,
                                        'level': 5,
                                        'midterm_score': 96,
                                        'midterm_weight': 50,
                                        'module_score': 96}}]
    Number of modules done: 10
    Scores so far: [95, 100, 98, 100, 80, 99, 87, 92, 96]

    Weighted average: 94.08 (ECTS: A, US: A)
    Unweighted average: 94.11 (ECTS: A, US: A)

    Classification: First Class Honours

    ECTS grade equivalence:
    { 'Algorithms and Data Structures I': 'A',
      'Algorithms and Data Structures II': 'A',
      'Discrete Mathematics': 'A',
      'Fundamentals of Computer Science': 'A',
      'How Computers Work': 'N/A',
      'Introduction to Programming I': 'A',
      'Introduction to Programming II': 'A',
      'Numerical Mathematics': 'A',
      'Object Oriented Programming': 'A',
      'Web Development': 'A'}

    US grade equivalence:
    { 'Algorithms and Data Structures I': 'A',
      'Algorithms and Data Structures II': 'A-',
      'Discrete Mathematics': 'A',
      'Fundamentals of Computer Science': 'A',
      'How Computers Work': 'N/A',
      'Introduction to Programming I': 'A',
      'Introduction to Programming II': 'A',
      'Numerical Mathematics': 'B-',
      'Object Oriented Programming': 'A',
      'Web Development': 'B+'}

    GPA: 4 (US) – 4 (UK)
    Total credits done: 150 / 360 (41.67%)

## For developers

### To run the test suite

    pip install -r requirements-dev.txt
    pytest

### To develop locally as a package

    python setup.py develop

Then the command `ugc` (short for `uol_grades_calculator`) becomes available on the command-line. Type `ugc --help` for more information.

### To publish to PyPI

Update version as necessary in `uol_grades_calculator/__init__.py` and `setup.py`.

Regenerate a build:

    rm -rf dist build
    python setup.py sdist bdist_wheel --universal

Test the package at test.pypi.org:

    python -m twine upload --repository testpypi dist/*

The package will be publicly available at https://test.pypi.org/project/uol-grades-calculator/ and you will be able to `pip install` it as usual.

Publish officially at [pypi.org](https://pypi.org):

    python -m twine upload dist/*
