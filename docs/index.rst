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

.. image:: https://img.shields.io/pypi/v/uol-grades-calculator.svg
  :target: https://pypi.python.org/pypi/uol-grades-calculator
  :alt: PyPi badge

.. image:: https://readthedocs.org/projects/uol-grades-calculator/badge/?version=latest
  :target: https://uol-grades-calculator.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

Simple script to get information about progress made in a BSc Computer Science at the University of London (calculations are specific to this particular degree).

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


Example output:

::

    $ ugc summarize progress

    Modules in progress:
    [ { 'Agile Software Projects': { 'completion_date': '2021-03',
                                    'level': 5,
                                    'midterm_score': 74,
                                    'midterm_weight': 30}},
        { 'Graphics Programming': { 'completion_date': '2021-03',
                                    'level': 5,
                                    'midterm_score': 96,
                                    'midterm_weight': 50}},
        { 'Programming with Data': { 'completion_date': '2021-03',
                                    'level': 5,
                                    'midterm_score': 84,
                                    'midterm_weight': 50}}]

    Weighted average (including modules in progress): 90.23
    ECTS: A
    US: A-

    Unweighted average (including modules in progress): 91.75
    ECTS: A
    US: A-

    Classification (weighted): First Class Honours

    ECTS grade equivalence:
    { 'Agile Software Projects': 'A',
        'Graphics Programming': 'A',
        'Programming with Data': 'A'}

    US grade equivalence:
    { 'Agile Software Projects': 'C',
        'Graphics Programming': 'A',
        'Programming with Data': 'B'}

    GPA (weighted): 3.7 US – 4 UK


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
