"""General utility functions for use in Fabfile or setup.py"""
import os
import sys
import typing as T
from contextlib import contextmanager
from pathlib import Path

import fabric


class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).
    '''

    def __init__(self):
        # Open a pair of null files
        self.null_fds = os.open(os.devnull, os.O_RDWR), os.open(os.devnull, os.O_RDWR)
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


@contextmanager
def set_env(**kwargs):
    """Set environment variables temporarily in current shell;
    export to those spawned by fabric."""
    for key, value in kwargs.items():
        os.environ[key] = value

    with fabric.api.shell_env(**kwargs):
        yield

    for key in kwargs:
        del os.environ[key]


@contextmanager
def append_to_path(*paths: T.Union[Path, str]):
    """Append the paths to sys.path temporarily."""
    for path in paths:
        if isinstance(path, str):
            sys.path.append(path)
        elif isinstance(path, Path):
            sys.path.append(
                str(path.absolute())
            )

    yield

    for path in paths:
        sys.path.pop()
