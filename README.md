# Grades Calculator

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

## To run the utility

      cd src
      python grades.py

## To run the test suite

      pip install -r requirements-dev.txt
      cd src
      pytest

## Skeleton `grades.json`

Sample format for any given module.

### Module taken

```json
      "Algorithms and Data Structures I": {
      "score": 80.5,
      "level": 4
      }
```

### Module recognized (RPL)

```json
"Algorithms and Data Structures I": {
    "score": -1,
    "level": 4
  }
```

### Complete sample JSON file

The following contains the complete list of modules to be taken, except for one elective module at level 6. Simply add the `score` property once a module has been taken care of. The "Final Project" module should be named as such and nothing else if you want it to count for 30 credits instead of 15 credits :wink:.

You should create the file `src/grades.json` and add to it the following content as a starter:

```json
{
  "Algorithms and Data Structures I": {
    "level": 4
  },
  "Discrete Mathematics": {
    "level": 4
  },
  "Fundamentals of Computer Science": {
    "level": 4
  },
  "How Computers Work": {
    "level": 4
  },
  "Introduction to Programming I": {
    "level": 4
  },
  "Computational Mathematics": {
    "level": 4
  },
  "Introduction to Programming II": {
    "level": 4
  },
  "Web Development": {
    "level": 4
  },
  "Algorithms and Data Structures II": {
    "level": 5
  },
  "Agile Software Projects": {
    "level": 5
  },
  "Computer Security": {
    "level": 5
  },
  "Databases, networks and the web": {
    "level": 5
  },
  "Graphics Programming": {
    "level": 5
  },
  "Object Oriented Programming": {
    "level": 5
  },
  "Programming with Data": {
    "level": 5
  },
  "Software Design and Development": {
    "level": 5
  },
  "Databases and Advanced Data Techniques": {
    "level": 6
  },
  "Machine Learning and Neural Networks": {
    "level": 6
  },
  "Artificial Intelligence": {
    "level": 6
  },
  "Intelligent Signal Processing": {
    "level": 6
  },
  "Natural Language Processing": {
    "level": 6
  },
  "ONE ELECTIVE": {
    "level": 6
  },
  "Final Project": {
    "level": 6
  }
}
```
