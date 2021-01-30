# Grades Calculator

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

---

## Table of contents

- [Grades Calculator](#grades-calculator)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [To run the utility](#to-run-the-utility)
  - [To run the test suite](#to-run-the-test-suite)
  - [Skeleton `grades.yml`](#skeleton-gradesyml)
    - [Module taken](#module-taken)
    - [Module recognized (RPL)](#module-recognized-rpl)
    - [Complete sample YAML file](#complete-sample-yaml-file)
  - [Sample output](#sample-output)

---

## Requirements

Python 3.6 and above.

## To run the utility

      pip install -r requirements.txt
      python main.py

## To run the test suite

      pip install -r requirements-dev.txt
      pytest

## Skeleton `grades.yml`

Sample format for any given module.

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

The included template `src/grades-template.yml` contains the complete list of modules to be taken, except for one elective module at level 6. Simply update the `module_score` property once a module has been taken. The "Final Project" module should be named as such and nothing else if you want it to count for 30 credits instead of 15 credits :wink:.

You should create the file `grades.yml` in this directory to get started. You can copy the available template like so:

    cp src/grades-template.yml grades.yml

## Sample output

    $ python main.py

    Modules taken:
    [ {'Algorithms and Data Structures I': {'level': 4, 'module_score': 95}},
      {'Discrete Mathematics': {'level': 4, 'module_score': 100}},
      {'Fundamentals of Computer Science': {'level': 4, 'module_score': 98}},
      {'How Computers Work': {'level': 4, 'module_score': -1}},
      {'Introduction to Programming I': {'level': 4, 'module_score': 100}},
      {'Numerical Mathematics': {'level': 4, 'module_score': 80}},
      {'Introduction to Programming II': {'level': 4, 'module_score': 99}},
      {'Web Development': {'level': 4, 'module_score': 87}},
      {'Algorithms and Data Structures II': {'level': 5, 'module_score': 92}},
      {'Object Oriented Programming': {'level': 5, 'module_score': 96}}]
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
