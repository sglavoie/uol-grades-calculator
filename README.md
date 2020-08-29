# Grades Calculator

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

## Requirements

Python 3.6 and above.

## To run the utility

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

