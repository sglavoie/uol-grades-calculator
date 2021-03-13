# Grades Calculator

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

---

## Table of contents

- [Grades Calculator](#grades-calculator)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [To run the utility](#to-run-the-utility)
  - [Skeleton `grades.yml`](#skeleton-gradesyml)
    - [Module taken](#module-taken)
    - [Module recognized (RPL)](#module-recognized-rpl)
    - [Complete sample YAML file](#complete-sample-yaml-file)
  - [Sample output](#sample-output)
  - [For developers](#for-developers)
    - [To run the test suite](#to-run-the-test-suite)
    - [To develop locally as a package](#to-develop-locally-as-a-package)

---

## Requirements

Python 3.6 and above. Install additional dependencies with the following command:

    pip install -r requirements.txt

## To run the utility

    python -m uol_grades_calculator

## Skeleton `grades.yml`

Each module described in `grades.yml` should contain information adhering to the following indications:

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

### Complete sample YAML file

The included template `uol_grades_calculator/grades-template.yml` contains the complete list of modules to be taken, except for one elective module at level 6. Simply update the `module_score` property once a module has been taken. The "Final Project" module should be named as such and nothing else if you want it to count for 30 credits instead of 15 credits :wink:.

You should create the file `grades.yml` in this directory to get started. You can copy the available template like so:

    cp uol_grades_calculator/grades-template.yml grades.yml

## Sample output

    $ python -m uol_grades_calculator summarize

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
