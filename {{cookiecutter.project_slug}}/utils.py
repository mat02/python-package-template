import json
from configparser import ConfigParser
from operator import attrgetter
from pathlib import Path
from types import SimpleNamespace
from functools import partial
from io import StringIO

from colorama import init, Back

init(autoreset=True)


def print_in_color(color, *args, **kwargs):
    """Print text in a given color"""
    file = kwargs.pop('file', None)
    with StringIO('w+') as fp:
        fp.write(color)
        print(*args, file=fp, **kwargs)
        fp.seek(0)
        print(fp.read().strip(), file=file)


print_red = partial(print_in_color, Back.RED)
print_green = partial(print_in_color, Back.GREEN)
print_yellow = partial(print_in_color, Back.YELLOW)


def _verify_lockfile():
    """Assert that all the packages in Pipfile are in Pipfile.lock"""

    config = ConfigParser()
    config.read('Pipfile')

    pipfile_packages = set(p.lower().replace('_', '-') for p, _ in
                           config.items('packages') + (
                               config.items('dev-packages') if config.has_section('dev-packages') else []))

    lockfile_data = json.loads(Path('Pipfile.lock').read_text())
    lockfile_packages = set(tuple(lockfile_data['default'].keys()) + tuple(lockfile_data['develop'].keys()))

    assert pipfile_packages.issubset(
        lockfile_packages), Back.RED + '{} package(s) in Pipfile not in Pipfile.lock - pipenv lock'. \
        format(pipfile_packages.difference(lockfile_packages))


def get_packages_from_lockfile():
    """
    Return object that contains default and development packages from Pipfile.lock

    Returns: SimpleNamespace(default=[...], development=[...])

    """

    result = SimpleNamespace(default=list(), development=list())
    lockfile = Path('Pipfile.lock')
    lockfile_data = json.loads(lockfile.read_text())
    for key in ('default', 'develop'):
        for package, version_info in lockfile_data[key].items():
            packages = attrgetter('development' if key == 'develop' else key)(result)
            packages.append(package + version_info['version'])
    return result
