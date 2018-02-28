#!/usr/bin/env python
"""Local project task runner"""
from contextlib import contextmanager
import subprocess as sp
import typing as T
import copy
import os

import click


def shell(command: str) -> sp.CompletedProcess:
    """Run the command in a shell."""
    user = os.getlogin()
    print(f'{user}: {command}')
    process = sp.run(command, shell=True)
    print()
    return process


@contextmanager
def env(**kwargs) -> dict:
    """Set environment variables and yield new environment dict."""
    original_environment = copy.deepcopy(os.environ)

    for key, value in kwargs.items():
        os.environ[key] = value

    yield os.environ

    for key in os.environ:
        if key not in original_environment:
            del os.environ[key]
        else:
            os.environ[key] = original_environment[key]


@contextmanager
def path(*paths: os.PathLike, prepend=False) -> T.List[str]:
    """
    Add the paths to $PATH and yield the new $PATH as a list.

    Args:
        prepend: prepend paths to $PATH else append
    """
    paths = list(paths)

    for index, _path in enumerate(paths):
        if not isinstance(_path, str):
            paths[index] = _path.__fspath__()
        elif '~' in _path:
            paths[index] = os.path.expanduser(_path)

    original_path = os.environ['PATH'].split(':')

    paths = paths + original_path if prepend else original_path + paths

    with env(PATH=':'.join(paths)):
        yield paths


@contextmanager
def cd(path: os.PathLike) -> os.PathLike:
    """Change the current working directory and yield the last cwd."""
    cwd = os.getcwd()
    os.chdir(path)
    yield cwd
    os.chdir(cwd)


@contextmanager
def quiet():
    """
    Suppress stdout and stderr.

    https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
    """

    # open null file descriptors
    null_file_descriptors = (
        os.open(os.devnull, os.O_RDWR),
        os.open(os.devnull, os.O_RDWR)
    )

    # save stdout and stderr
    stdout_and_stderr = (os.dup(1), os.dup(2))

    # assign the null pointers to stdout and stderr
    null_fd1, null_fd2 = null_file_descriptors
    os.dup2(null_fd1, 1)
    os.dup2(null_fd2, 2)

    yield

    # re-assign the real stdout/stderr back to (1) and (2)
    stdout, stderr = stdout_and_stderr
    os.dup2(stdout, 1)
    os.dup2(stderr, 2)

    # close all file descriptors.
    for fd in null_file_descriptors + stdout_and_stderr:
        os.close(fd)


@click.group()
def main():
    """Project tasks."""
    pass


if __name__ == '__main__':
    main()
