Requirements
============

Python 3.6 and above. This is it!


Install and uninstall
=====================

The most straightforward way to use this tool would be to install it `from PyPI <https://pypi.org/project/uol-grades-calculator/>`_ by typing the following in a terminal (use of `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ recommended!)::

    $ pip install uol-grades-calculator


Reversing the process is a matter of typing this::

    $ pip uninstall uol-grades-calculator


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


How to use this tool
====================

Please refer to the page :doc:`commands` to see what ``ugc`` can do for you.

Demo
====

.. raw:: html

    <!-- Demo of v0.5.2 -->
    <script id="asciicast-vPb76ILpzp2d38DbOQngrlxmm" src="https://asciinema.org/a/vPb76ILpzp2d38DbOQngrlxmm.js" async></script>
