#!/usr/bin/env python
from pathlib import Path
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def install_hooks():
    """
    Install git hooks to make life easier.
    """
    hooks_path = Path('{{cookiecutter.project_slug}}/.git/hooks/')

    os.makedirs(hooks_path, exist_ok=True)

    pre_push_path = Path(hooks_path, 'pre-push')

    pre_push_path.write_text('{{cookiecutter.project_slug}} dev test')


if __name__ == '__main__':

    open_source = '{{ cookiecutter.open_source }}'.lower()
    if not open_source == 'y' or open_source == 'yes':
        remove_file('LICENSE')

    install_hooks()
