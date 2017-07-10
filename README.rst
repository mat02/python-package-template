=============================
Python 3 package cookiecutter
=============================

.. image:: https://pyup.io/repos/github/knowsuchagency/cookiecutter-pypackage/shield.svg
     :target: https://pyup.io/repos/github/knowsuchagency/cookiecutter-pypackage/
     :alt: Updates

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

* Create a repo and put it there.
* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. ``pipenv install --dev``) || ``pip install .[dev]``
* Activate your project on `pyup.io`_. Use ``fab gen_requirements_txt`` to generate requirements.txt from Pipfile.


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
.. _`cookiecutter-package`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Click`: http://click.pocoo.org/
