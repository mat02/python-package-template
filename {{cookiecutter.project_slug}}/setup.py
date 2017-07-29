#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import json
from configparser import ConfigParser
from operator import attrgetter
from pathlib import Path
from types import SimpleNamespace

from setuptools import setup


def verify_lockfile():
    """Assert that all the packages in Pipfile are in Pipfile.lock ."""
    config = ConfigParser()
    config.read('Pipfile')

    pipfile_packages = set(p.lower().replace('_', '-') for p, _ in
                           config.items('packages') + (
                               config.items('dev-packages') if config.has_section('dev-packages') else []))

    lockfile_data = json.loads(Path('Pipfile.lock').read_text())
    lockfile_packages = set(tuple(lockfile_data['default'].keys()) + tuple(lockfile_data['develop'].keys()))

    assert pipfile_packages.issubset(
        lockfile_packages), '{} packages in Pipfile not in Pipfile.lock - Please update Pipfile.lock'. \
        format(pipfile_packages.difference(lockfile_packages))


def get_packages_from_lockfile():
    result = SimpleNamespace(default=list(), development=list())
    lockfile = Path('Pipfile.lock')
    lockfile_data = json.loads(lockfile.read_text())
    for key in ('default', 'develop'):
        for package, version_info in lockfile_data[key].items():
            packages = attrgetter('development' if key == 'develop' else key)(result)
            packages.append(package + version_info['version'])
    return result


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
