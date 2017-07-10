Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. include:: ../README.rst

{% if cookiecutter.cli.lower() == 'y' or cookiecutter.cli.lower() == 'yes' %}
Command Line Interface
----------------------

.. include:: ../{{ cookiecutter.project_slug }}/cli.py
    :start-after: """
    :end-before: """
    :literal:
{% endif %}

API Documentation
-----------------

.. include:: modules.rst
    :start-line: 2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
