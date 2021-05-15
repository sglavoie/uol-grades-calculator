For developers
==============

Getting a copy of the source code
---------------------------------

`Clone <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository>`_ this `repository <https://github.com/sglavoie/uol-grades-calculator>`_.


Running the test suite
----------------------

.. code-block:: bash

    $ pip install -r requirements-dev.txt
    $ pytest


Developing locally as a package
-------------------------------

Installing the necessary requirements:

.. code-block:: bash

    $ pip install -r requirements.txt


Building the application once (no need to rebuild to test changes on the source code):

.. code-block:: bash

    $ python setup.py develop


Then the command ``ugc`` (short for ``uol_grades_calculator``) becomes available on the command-line. Type ``ugc --help`` for more information.

The tool can then be uninstalled using the following command:

.. code-block:: bash

    $ python setup.py develop --uninstall


Generating modules documentation
--------------------------------

.. code-block:: bash

    $ cd docs/
    $ sphinx-apidoc -f -M -P -d 1 -o ./source ../uol_grades_calculator


.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Flag
     - Description
   * - ``-f``
     - overwrite existing files
   * - ``-M``
     - put module documentation before submodule
   * - ``-P``
     - include "_private" modules
   * - ``-o``
     - output directory (``docs/source/``)
   * - ``-d``
     - maximum depth of submodules to show in the TOC
