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
