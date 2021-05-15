.. toctree::
    :hidden:

    developers


Available commands
==================

``check``
---------

::

    $ ugc check --help

    Usage: ugc check [OPTIONS] COMMAND [ARGS]...

    Perform sanity checks against the results generated.

    Options:
    --help  Show this message and exit.

    Commands:
    score-accuracy  Check for rounding errors when averaging module score.


``check score-accuracy``
------------------------

::

    $ ugc check score-accuracy --help

    Usage: ugc check score-accuracy [OPTIONS]

    Check for rounding errors when averaging module score.

    Options:
    --help  Show this message and exit.


Example output::

    $ ugc check score-accuracy

    Algorithms and Data Structures I: 78% actual [expected 79.0%]
    Discrete Mathematics: 79.5% actual [expected 80.0%]
    Fundamentals of Computer Science: 60% actual [expected 58.0%]


``generate-sample``
-------------------

::

    $ ugc generate-sample --help

    Usage: ugc generate-sample [OPTIONS]

    Generate a sample grades YAML config file.

    Options:
    -f, --force-overwrite  Overwrite the existing config file, if any.
    --help                 Show this message and exit.


Example output::

    $ ugc generate-sample

    Configuration file not found: /home/sglavoie/.grades.yml
    → Configuration file generated.


``summarize``
-------------

::

    $ ugc summarize --help

    Usage: ugc summarize [OPTIONS] COMMAND [ARGS]...

        Print a summary of the progress made so far.

    Options:
        --help  Show this message and exit.

    Commands:
        all       Output includes modules done as well as those in progress.
        done      Output includes only modules that are done and dusted.
        progress  Output includes only modules that are in progress.


Example output::

    $ ugc summarize done

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

    Weighted average: 94.08
    ECTS: A
    US: A

    Unweighted average: 94.11
    ECTS: A
    US: A

    Classification (weighted): First Class Honours

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

    GPA (weighted): 4 US – 4 UK
    Total credits done: 150 / 360 (41.67%)
