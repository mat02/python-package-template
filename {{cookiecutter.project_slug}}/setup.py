#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from utils import _verify_lockfile as verify_lockfile
from utils import get_packages_from_lockfile

from setuptools import setup

# ensure all the packages listed in Pipfile are in Pipfile.lock
verify_lockfile()

# read the lockfile to get default and development packages
default, development = get_packages_from_lockfile()

setup(
    install_requires=default,
    tests_require=development,
    extras_require={
        'dev': development,
        'development': development,
        'test': development,
        'testing': development,
    },
    {% if cookiecutter.cli.lower() == 'y' or cookiecutter.cli.lower() == 'yes' %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main'
        ]
    },
    {% endif %}
)
