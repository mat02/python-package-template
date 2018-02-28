#!/usr/bin/env python
"""Task runner for the {{ cookiecutter.package_name }} project."""
from tempfile import NamedTemporaryFile
from contextlib import contextmanager
from textwrap import dedent
from pathlib import Path
import subprocess as sp
import typing as T
import copy
import os
import re

import click


def shell(command: str, check=True) -> sp.CompletedProcess:
    """
    Run the command in a shell.

    Args:
        command: the command to be run
        check: raise exception if return code not zero

    Returns: Completed Process

    """
    user = os.getlogin()
    print(f'{user}: {command}')
    process = sp.run(command, check=check, shell=True)
    print()
    return process


@contextmanager
def cd(path_: T.Union[os.PathLike, str]):
    """Change the current working directory."""
    cwd = os.getcwd()
    os.chdir(path_)
    yield
    os.chdir(cwd)


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

    # ensure we're running commands from project root

    root = Path(__file__).parent.absolute()
    cwd = Path().absolute()

    if root != cwd:
        raise EnvironmentError(os.linesep.join(map(
            str, ('', 'You should running this from', root, "You're currently in", cwd))))


def release():
    """Package and upload a release to pypi."""
    context = click.get_current_context()
    for command in (test_readme_rst, clean, tox, publish_docs):
        context.invoke(command)
    shell('python setup.py sdist bdist_wheel')
    shell('twine upload dist/*')


@main.command()
def dist():
    """Build source and wheel package."""
    context = click.get_current_context()
    context.invoke(clean)
    shell('python setup.py sdist')
    shell('python setup.py bdist_wheel')


@main.command()
def uninstall():
    """Uninstalls all Python dependencies."""

    patt = re.compile(r'\w+=(\w+)')

    packages = []

    for line in sp.run(('pip', 'freeze'), stdout=sp.PIPE).stdout.decode().splitlines():
        if '==' in line:
            package, *_ = line.split('==')

        match = patt.search(line)

        if match:
            *_, package = match.groups()

        packages.append(package)

    stdin = os.linesep.join(packages).encode()

    with NamedTemporaryFile() as fn:
        fn.write(stdin)
        fn.seek(0)
        shell(f'cat {fn.name} | xargs pip uninstall -y')


@main.command()
@click.option('--development/--no-development', default=True, help='install development requirements.')
@click.option('--idempotent/--no-idempotent', default=True, help='uninstall current packages before installing.')
def install(development, idempotent):
    """
    Install Python dependencies.
    """
    context = click.get_current_context()
    if idempotent:
        context.invoke(uninstall)

    development_flag = '-d' if development else ''

    shell(f'pipenv install {development_flag}')
    shell('python setup.py develop')


@main.command()
def autopep8():
    """Autopep8 modules."""
    shell('autopep8 -i -r fabfile.py {{ cookiecutter.project_slug }}/ tests/')


@main.command()
def test_readme_rst():
    """Test README.rst to ensure it will render correctly in warehouse."""
    shell('python setup.py check -r -s')


@main.command()
def clean_build():
    """Remove build artifacts."""
    shell('rm -fr build/')
    shell('rm -fr dist/')
    shell('rm -rf .eggs/')
    shell("find . -name '*.egg-info' -exec rm -fr {} +")
    shell("find . -name '*.egg' -exec rm -f {} +")


@main.command()
def clean_pyc():
    """Remove Python file artifacts."""
    shell("find . -name '*.pyc' -exec rm -f {} +")
    shell("find . -name '*.pyo' -exec rm -f {} +")
    shell("find . -name '*~' -exec rm -f {} +")
    shell("find . -name '__pycache__' -exec rm -fr {} +")


@main.command()
def clean_test():
    """Remove test and coverage artifacts."""
    shell('rm -fr .tox/')
    shell('rm -f .coverage')
    shell('rm -fr htmlcov/')


@main.command()
def clean():
    """Remove all build, test, coverage and Python artifacts."""
    context = click.get_current_context()
    for command in (clean_build, clean_pyc, clean_test):
        context.invoke(command)


@main.command()
@click.option('--capture/--no-capture', default=False, help='capture stdout')
@click.option('--pdb', is_flag=True, help='enter debugger on test failure')
def test(capture, pdb):
    """
    Run tests quickly with default Python.
    """
    flags = ' '.join([
        '-s' if not capture else '',
        '--pdb' if capture else ''
    ])
    shell('py.test tests/' + ' ' + flags)


@main.command()
def tox():
    """Run tests in isolated environments using tox."""
    shell('tox')


@main.command()
@click.option('--no-browser', is_flag=True, help="Don't open browser after building report.")
def coverage(no_browser):
    """Check code coverage quickly with the default Python."""
    shell('coverage run --source {{ cookiecutter.project_slug }} -m pytest')
    shell('coverage report -m')
    shell('coverage html')

    if no_browser:
        return

    shell('open htmlcov/index.html')


@main.command()
@click.option('--no-browser', is_flag=True, help="Don't open browser after building docs.")
def docs(no_browser):
    """
    Generage Sphinx HTML documentation, including API docs.
    """
    shell('rm -f docs/{{ cookiecutter.project_slug }}.rst')
    shell('rm -f docs/modules.rst')
    shell('rm -f docs/{{ cookiecutter.project_slug }}*')
    shell('sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}')

    with cd('docs'):
        shell('make clean')
        shell('make html')

    shell('cp -rf docs/_build/html/ public/')

    if no_browser:
        return

    shell('open public/index.html')


@main.command()
def publish_docs():
    """
    Compile docs and publish to GitHub Pages.

    Logic borrowed from `hugo <https://gohugo.io/tutorials/github-pages-blog/>`
    """

    if shell('git diff-index --quiet HEAD --', check=False).status_code != 0:
        shell('git status')
        raise EnvironmentError('The working directory is dirty. Please commit any pending changes.')

    if shell('git show-ref refs/heads/gh-pages', check=False).status_code != 0:
        # initialized github pages branch
        shell(dedent("""
            git checkout --orphan gh-pages
            git reset --hard
            git commit --allow-empty -m "Initializing gh-pages branch"
            git push gh-pages
            git checkout master
            """).strip())
        print('created github pages branch')

    # deleting old publication
    shell('rm -rf public')
    shell('mkdir public')
    shell('git worktree prune')
    shell('rm -rf .git/worktrees/public/')
    # checkout out gh-pages branch into public
    shell('git worktree add -B gh-pages public gh-pages')
    # generating docs
    context = click.get_current_context()
    context.invoke(docs, no_browser=True)
    # push to github
    with cd('public'):
        shell('git add .')
        shell('git commit -m "Publishing to gh-pages (Fabfile)"')
        shell('git push origin gh-pages')


if __name__ == '__main__':
    main()
