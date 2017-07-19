{% set open_source = cookiecutter.open_source.lower() == 'y' or cookiecutter.open_source.lower() == 'yes' -%}


{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

.. image:: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/
     :alt: Updates

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg

{% endif %}

{{ cookiecutter.project_short_description }}

{% if open_source %}
* Documentation: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}
* Source: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
{% endif %}

Installation
--------

* TODO

Usage
---------

* TODO
