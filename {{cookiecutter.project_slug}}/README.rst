{% set open_source = cookiecutter.open_source.lower() == 'y' or cookiecutter.open_source.lower() == 'yes' -%}


{% for _ in cookiecutter.package_name %}={% endfor %}
{{ cookiecutter.package_name }}
{% for _ in cookiecutter.package_name %}={% endfor %}

{% if open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}

.. image:: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/
     :alt: Updates

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg

{% endif %}

{{ cookiecutter.project_short_description }}

{% if open_source %}
* Documentation: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.package_name }}
* Source: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}
{% endif %}

Installation
------------

::

    git clone {this repo}
    cd project_directory
    # activate your venv i.e.
    pipenv shell
    pip install -e .[dev]

Usage
---------

Use Pipenv to install new modules so they're tracked correctly in the Pipfile::

    pipenv install new-package

To run the app locally and/or deploy to cloudfoundry::

    {{cookiecutter.project_slug}} runserver
    {{cookiecutter.project_slug}} dev deploy
