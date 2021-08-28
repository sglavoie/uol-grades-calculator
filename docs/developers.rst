For developers
==============

Getting a copy of the source code
---------------------------------

`Clone <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository>`_ this `repository <https://github.com/sglavoie/uol-grades-calculator>`_.


Developing locally as a package
-------------------------------

Installing the necessary requirements:

.. code-block:: bash

    $ pip install -r requirements.txt -r requirements-dev.txt


Building the application once (no need to rebuild to test changes on the source code):

.. code-block:: bash

    $ python setup.py develop


Then the command ``ugc`` (short for ``uol grades calculator``) becomes available on the command-line. Type ``ugc --help`` for more information.

The tool can then be uninstalled using the following command:

.. code-block:: bash

    $ python setup.py develop --uninstall


Running the test suite
----------------------

Default settings are defined in ``pytest.ini``. Then, it's just a matter of typing:

.. code-block:: bash

    $ pytest


Managing dependencies
---------------------

- Requirements to test and develop the application should go into ``requirements-dev.txt``. None of these are required to run ``ugc`` as a user.
- User requirements should go into ``requirements.txt``.
- The section ``install_requires`` in ``setup.cfg`` should be kept up-to-date when new releases are to be published.
- Non-Python files (e.g. JSON) used by ``ugc`` should be explicitly included in ``MANIFEST.in`` to be distributed with the package.


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


Installing package from PyPI
----------------------------

Install from `test.pypi.org <https://test.pypi.org/project/uol-grades-calculator/>`_:

- Activate a virtual environment, then:

.. code-block:: bash

    # Latest version
    pip install -i https://test.pypi.org/simple/ uol-grades-calculator

    # Specific version
    pip install -i https://test.pypi.org/simple/ uol-grades-calculator==x.y.z


Test as a module:

.. code-block:: bash

    python -m ugc


Install from `pypi.org <https://pypi.org/project/uol-grades-calculator/>`_:

.. code-block:: bash

    # Latest version
    pip install uol-grades-calculator

    # Specific version
    pip install uol-grades-calculator==x.y.z


Adding ``ugc`` as a command
---------------------------

To avoid having to activate a virtual environment and calling the program as a module via ``python -m ugc``, one can create an alias or put a symbolic link in the ``$PATH`` to make the command ``ugc`` accessible.

Creating an alias
.................

As a quick and dirty way to access ``ugc`` with an alias, a virtual environment can be activated and the Python interpreter can be called from that environment. Adding an alias like the following would do the trick:

.. code-block:: bash

    # Add to `~/.bash_aliases` or equivalent on your system
    alias ugc=". /tmp/.venv/bin/activate && python -m ugc"


Adding to the ``$PATH``
.......................

When developing locally and assuming all dependencies were installed inside a virtual environment:

.. code-block:: bash

    # Make sure the `ugc` package was installed to allow editing source code
    # on the fly:
    python setup.py develop

    # Create a symbolic link from your virtual environment to a directory
    # in your path. You can print it to see what it looks like:
    echo $PATH

    # For instance, if ~/.local/bin is in $PATH, something as follows would
    # work, assuming the virtual environment is named `.venv`:
    ln -s /path/to/uol_grades_calculator/.venv/bin/ugc ~/.local/bin/ugc

    # Then `ugc` can be called as a regular program:
    ugc


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
