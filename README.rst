=============================
Python 3 Package Cookiecutter
=============================

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg

An opinionated, dead-simple cookiecutter_ for modern Python 3 packages.

*Adapted from Audrey's* cookiecutter-pypackage_


Features
--------

* Testing setup with ``py.test``
* Future-proof use of Pipfile_ as opposed to requirements.txt [see pipenv_]
* Tox_ testing: Setup to easily test
* Sphinx_ docs: Documentation ready for generation and hosting on `GitHub Pages`_
* Bumpversion_: Pre-configured version bumping with a single command
* Command line interface with Click_

Quickstart
----------

Install the latest `Cookiecutter`_ and `pipenv`_ (optional, but highly recommended) if you haven't installed it yet.

.. code-block:: bash

    brew install cookiecutter pipenv


Generate a Python package project

.. code-block:: bash

    cookiecutter https://github.com/knowsuchagency/python-package-template.git --checkout cloudfoundry

    # answer questions to generate project template

    cd your_new_project

    # generate the virtual environment and activate it

    pipenv shell # or whatever you use to manage your venvs

    # install package dependencies within venv

    pip install -e .[dev]

The last step will install the task runner at the root of the repo, `run.py`_ as a command-line
utility ``{{project_slug}} dev``.

    # to run the development server locally

    {{project_slug}} runserver

    # deploy

    {{project_slug}} dev deploy

Development
-----------

You should now have a command-line tool ``{{project_slug}} dev`` which you can use to execute common tasks.

This is just a shortcut to the `run.py`_ file at the root of your project,
meaning you have 3 ways of executing the task runner::

    {{project_slug}} dev

    # or, from project root

    ./run.py

    # or

    python -m run

The following are some of the sub-commands you may find::

    Commands:
      autopep8      Autopep8 modules.
      clean         Remove all build, test, coverage and Python...
      coverage      Check code coverage quickly with the default...
      dist          Build source and wheel package.
      docs          Generate Sphinx HTML documentation, including...
      install       Install Python dependencies.
      publish_docs  Compile docs and publish to GitHub Pages.
      test          Run tests quickly with default Python.
      test_readme   Test README.rst to ensure it will render...
      tox           Run tests in isolated environments using tox.
      uninstall     Uninstalls all Python dependencies.


Additional Options
------------------

* Create a GitHub repo for your generated project.
* Add the repo to your Travis-CI_ account.
* Activate your project on `pyup.io`_. (if using pipenv, you can generate requirements.txt with ``pipenv lock -r``)


.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _PyPi: https://pypi.python.org/pypi
.. _`pipfile`: https://github.com/pypa/pipfile
.. _`github pages`: https://pages.github.com/
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Click`: http://click.pocoo.org/
.. _`pipenv`: http://docs.pipenv.org/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _run.py: {{cookiecutter.project_slug}}/run.py
