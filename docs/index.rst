.. UoL Grades Calculator documentation master file, created by
   sphinx-quickstart on Fri May 14 19:24:42 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to UoL Grades Calculator's documentation!
*************************************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Grades Calculator
=================

This tool is all about getting information and generating insights from the progress made in a `BSc Computer Science at the University of London <https://london.ac.uk/courses/computer-science>`_ (calculations are specific to this particular degree).

Requirements
============

Python 3.6 and above. Install additional dependencies with the following command:

.. code-block:: bash

    $ pip install -r requirements.txt


To run the utility
==================

.. code-block:: bash

    $ ugc


By passing no arguments, this will print the default help message.

Generate a sample config file to get started
============================================

To generate a sample configuration file, run the following command:

.. code-block:: bash

    $ ugc generate-sample


The configuration file will be created in your home directory as a hidden file (i.e. ``~/.grades.yml``).

Specifying a different path for the config file
-----------------------------------------------

If you want to create it somewhere else:

.. code-block:: bash

    $ ugc --config /path/to/config/file.yml generate-sample


Note that you will have to indicate where the config is each time you use this tool in this case (you can always create an alias to avoid the trouble of typing it every time). For example:

.. code-block:: bash

    $ ugc --config /path/to/config/file.yml summarize


How to fill the config file (`.grades.yml` by default)
------------------------------------------------------

Each module described in the config file should contain information adhering to the following indications:

.. csv-table:: Configuration options
    :file: ./config_file.csv
    :widths: 25, 25, 25, 25
    :header-rows: 1

\* If a node value is left empty (or the node is absent in a given module), this will affect how the module is taken into account (average across all modules, summary of modules taken, etc.).

Here is a complete example for one module:

.. code-block:: yaml

    Algorithms and Data Structures I:
      completion_date: 2020-03
      final_score: 92
      final_weight: 50
      midterm_score: 98
      midterm_weight: 50
      module_score: 95
      level: 4


Module taken
............

This means we define a module score between `0` and `100`, both being inclusive values.

.. code-block:: yaml

    Algorithms and Data Structures I:
      module_score: 80.5


Module recognized (RPL)
.......................

In this case, we define a score of `-1` to indicate that this module is done but we didn't get a score for it.

.. code-block:: yaml

    Algorithms and Data Structures I:
      module_score: -1

Available commands
------------------

``check``
.........

::

    $ ugc check --help

    Usage: ugc check [OPTIONS] COMMAND [ARGS]...

    Perform sanity checks against the results generated.

    Options:
    --help  Show this message and exit.

    Commands:
    score-accuracy  Check for rounding errors when averaging module score.


``check score-accuracy``
........................

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
...................

::

    $ ugc generate-sample --help

    Usage: ugc generate-sample [OPTIONS]

    Generate a sample grades YAML config file.

    Options:
    -f, --force-overwrite  Overwrite the existing config file, if any.
    --help                 Show this message and exit.


Example output::

    Configuration file not found: /home/sglavoie/.grades.yml
    → Configuration file generated.


``summarize``
.............

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


For developers
==============

To run the test suite
---------------------

.. code-block:: bash

    $ pip install -r requirements-dev.txt
    $ pytest


To develop locally as a package
-------------------------------

.. code-block:: bash

    $ python setup.py develop


Then the command ``ugc`` (short for ``uol_grades_calculator``) becomes available on the command-line. Type ``ugc --help`` for more information.
