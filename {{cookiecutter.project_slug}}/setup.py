#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from utils import verify_lockfile, get_packages_from_lockfile

from setuptools import setup

verify_lockfile()

packages = get_packages_from_lockfile()

setup(
    install_requires=packages.default,
    tests_require=packages.development,
    extras_require={
        'dev': packages.development,
        'development': packages.development,
        'test': packages.development,
        'testing': packages.development,
    },
    {% if cookiecutter.cli.lower() == 'y' or cookiecutter.cli.lower() == 'yes' %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main'
        ]
    },
    {% endif %}
)
