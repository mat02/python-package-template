=============================
Python 3 Package Cookiecutter
=============================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg

A dead-simple and opinionated cookiecutter for modern Python 3 packages.

Adapted from Audrey's cookiecutter-pypackage_


Features
--------

* Testing setup with ``py.test``
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 3.5, 3.6
* Sphinx_ docs: Documentation ready for generation and hosting on `GitHub Pages`_
* Bumpversion_: Pre-configured version bumping with a single command
* Fabric_ for task automation
* Future-proof use of Pipfile_ as opposed to requirements.txt
* Optional command line interface with Docopt_.
  The cli module's docstring is automatically added to project documentation via Sphinx_.
  More robust cli applications may want to check out Click_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/knowsuchagency/cookiecutter-pypackage.git

Then:

* Create a GitHub repo for your generated project.
* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. ``pipenv install --dev``) || ``pip install .[dev]``
* Activate your project on `pyup.io`_. Use ``fab gen_requirements_txt`` to generate requirements.txt from Pipfile.

Upon creating your project, these are some of the options that will be available to you via the generated fabfile.
Prepend ``fab`` to the following commands from project root:

.. code-block:: bash

    clean                 Remove all build, test, coverage and Python artifacts.
    coverage              Check code coverage quickly with the default Python.
    docs                  Generage Sphinx HTML documentation, including API docs.
    gen_requirements_txt  Generate a requirements.txt from Fabfile.
    publish_docs          Compile docs and publish to GitHub Pages.
    release               Package and upload a release to pypi.
    test                  Run tests quickly with default Python.
    test_all              Run on multiple Python versions with tox.


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
.. _`docopt`: https://github.com/docopt/docopt
.. _`github pages`: https://pages.github.com/
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Click`: http://click.pocoo.org/
