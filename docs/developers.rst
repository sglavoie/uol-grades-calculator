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
    $ pip install -r requirements-dev.txt


Building the application once (no need to rebuild to test changes on the source code):

.. code-block:: bash

    $ python setup.py develop


Then the command ``ugc`` (short for ``uol grades calculator``) becomes available on the command-line. Type ``ugc --help`` for more information.

The tool can then be uninstalled using the following command:

.. code-block:: bash

    $ python setup.py develop --uninstall


Managing dependencies
---------------------

- Requirements to test and develop the application should go into ``requirements-dev.txt``. None of these are required to run ``ugc`` as a user.
- User requirements should go into ``requirements.txt``.
- The section ``install_requires`` in ``setup.cfg`` should be kept up-to-date when new releases are to be published.
- Non-Python files (e.g. YML and JSON) used by ``ugc`` should be explicitly included in ``MANIFEST.in`` to be distributed with the package.


Publishing the package to PyPI
------------------------------

.. code-block:: bash

    # Remove existing distribution packages
    rm -rf dist build

    # The following commands would be run preferably
    # from a virtual environment

    # Generate the distribution packages for PyPI
    python setup.py sdist bdist_wheel --universal

    # Upload to the test instance of PyPI
    python -m twine upload --repository testpypi dist/*

    # Upload to the production instance of PyPI
    python -m twine upload dist/*


Documentation
-------------

Generating modules documentation
................................

.. code-block:: bash

    $ cd docs/
    $ make docs


.. list-table:: Current options passed to build the docs
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
     - maximum depth of submodules to show in the TOC (set to ``1``)
   * - ``-T``
     - do not add a TOC for the modules


Rebuilding documentation
........................

.. code-block:: bash

    $ cd docs/
    $ make html


If something is not rendered even after a force-refresh (such as when editing the config file or adding custom CSS), try running ``make clean html`` instead: there can be instances where changes are not applied due to the local cache.
