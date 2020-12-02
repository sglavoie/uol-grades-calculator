# Grades Calculator

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

---

## Table of contents

- [Grades Calculator](#grades-calculator)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [To run the utility](#to-run-the-utility)
  - [To run the test suite](#to-run-the-test-suite)
  - [Skeleton `grades.json`](#skeleton-gradesjson)
    - [Module taken](#module-taken)
    - [Module recognized (RPL)](#module-recognized-rpl)
    - [Complete sample JSON file](#complete-sample-json-file)
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

## Skeleton `grades.json`

Sample format for any given module.

### Module taken

This means we define a score between `0` and `100`, both being inclusive values.

```json
      "Algorithms and Data Structures I": {
      "score": 80.5,
      "level": 4
      }
```

### Module recognized (RPL)

In this case, we define a score of `-1` to indicate that this module is done but we didn't get a score for it.

```json
"Algorithms and Data Structures I": {
    "score": -1,
    "level": 4
  }
```

### Complete sample JSON file

The included template `src/grades-template.json` contains the complete list of modules to be taken, except for one elective module at level 6. Simply add the `score` property once a module has been taken. The "Final Project" module should be named as such and nothing else if you want it to count for 30 credits instead of 15 credits :wink:.

You should create the file `grades.json` in this directory to get started. You can copy the available template like so:

    cp src/grades-template.json grades.json

## Sample output

    $ python main.py

    Modules taken:
    [ { 'Algorithms and Data Structures I': { 'level': 4,
                                              'score': 95}},
      { 'Discrete Mathematics': { 'level': 4,
                                  'score': 100}},
      { 'How Computers Work': { 'level': 4,
                                'score': -1}},
      { 'Introduction to Programming I': { 'level': 4,
                                           'score': 100}},
      { 'Numerical Mathematics': { 'level': 4,
                                   'score': 80}},
      { 'Introduction to Programming II': { 'level': 4,
                                            'score': 99}},
      { 'Web Development': { 'level': 4,
                             'score': 87}}]
    Number of modules done: 7
    Scores so far: [95, 100, 100, 80, 99, 87]
    Average so far: 93.5 (ECTS: A, US: A)
    Classification: First Class Honours
    ECTS grade equivalence:
    { 'Algorithms and Data Structures I': 'A',
      'Discrete Mathematics': 'A',
      'How Computers Work': 'N/A',
      'Introduction to Programming I': 'A',
      'Introduction to Programming II': 'A',
      'Numerical Mathematics': 'A',
      'Web Development': 'A'}
    US grade equivalence:
    { 'Algorithms and Data Structures I': 'A',
      'Discrete Mathematics': 'A',
      'How Computers Work': 'N/A',
      'Introduction to Programming I': 'A',
      'Introduction to Programming II': 'A',
      'Numerical Mathematics': 'B-',
      'Web Development': 'B+'}
    GPA: 4 (US) – 4 (UK)
    Total credits done: 105 / 360 (29.17%)
