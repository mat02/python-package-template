=============================
Python 3 Package Cookiecutter
=============================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg

An opinionated, dead-simple cookiecutter_ for modern Python 3 packages.

*Adapted from Audrey's* cookiecutter-pypackage_


Features
--------

* Testing setup with ``py.test``
* Future-proof use of Pipfile_ as opposed to requirements.txt [see pipenv_]
* Tox_ testing: Setup to easily test
* Sphinx_ docs: Documentation ready for generation and hosting on `GitHub Pages`_
* Bumpversion_: Pre-configured version bumping with a single command
* Fabric_ for task automation
* Command line interface with Click_

Quickstart
----------

Install the latest `Cookiecutter`_ and `pipenv`_ if you haven't installed them yet.

.. code-block:: bash

    brew install cookiecutter pipenv


Generate a Python package project

.. code-block:: bash

    cookiecutter https://github.com/knowsuchagency/launchpad.git

    # answer questions to generate project template

    cd your_new_project

    # To install dependencies...

    pipenv shell
    pipenv install -d
    python setup.py develop

    # to see what options are automated for you via fabric
    fab -l

Development
-----------

Upon creating your project and installing the requirements necessary for development, these are some of the options fabric_
will provide via the generated fabfile.

Prepend ``fab`` to the following commands from project root:

.. code-block:: bash

    deploy                Deploy to cloudfoundry.
    clean                 Remove all build, test, coverage and Python artifacts.
    clean_build           Remove build artifacts.
    clean_pyc             Remove Python file artifacts.
    clean_test            Remove test and coverage artifacts.
    coverage              Check code coverage quickly with the default Python.
    dist                  Build source and wheel package.
    docs                  Generage Sphinx HTML documentation, including API docs.
    test                  Run tests quickly with default Python.
    tox                   Run on multiple Python versions with tox.


For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _PyPi: https://pypi.python.org/pypi
.. _`pipfile`: https://github.com/pypa/pipfile
.. _`fabric`: http://www.fabfile.org/
.. _`github pages`: https://pages.github.com/
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Click`: http://click.pocoo.org/
.. _`pipenv`: http://docs.pipenv.org/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
