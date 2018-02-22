from functools import singledispatch
from contextlib import contextmanager
from pathlib import Path
import typing as T
import sys
import os

import fabric
from fabric.api import *


@task
def install(development=True, idempotent=True):
    """
    Install Python dependencies.

    Args:
        development: install self in development mode
        idempotent: run uninstall first
    """
    if true(idempotent):
        uninstall()

    development_flag = '-d' if true(development) else ''

    local(f'pipenv install {development_flag}')


@task
def uninstall():
    """Uninstalls all Python dependencies."""
    from tempfile import NamedTemporaryFile
    import subprocess as sp
    import os

    packages = []

    for line in sp.run(('pip', 'freeze'), stdout=sp.PIPE).stdout.decode().splitlines():
        if '==' in line:
            package, *_ = line.split('==')
        elif '#egg=' in line:
            *_, package = line.split('egg=')
        packages.append(package)

    stdin = os.linesep.join(packages).encode()

    with NamedTemporaryFile() as fn:
        fn.write(stdin)
        fn.seek(0)
        sp.run(f'cat {fn.name} | xargs pip uninstall -y', shell=True)


@task
def autopep8(only_modified=True):
    """Autopep8 modules."""
    if only_modified:
        local("git ls-files -m | grep '.py$' | xargs autopep8 -i")
    else:
        local('autopep8 -i -r fabfile.py {{ cookiecutter.project_slug }}/ tests/')


@task
def deploy():
    """Deploy to cloudfoundry."""
    try:
        print('freezing only required deps')

        uninstall()

        local('pipenv install')

        print('dependencies frozen')

        print('vendoring dependencies')

        local('rm -rf vendor')
        local('mkdir -p vendor')

        local('pip freeze > requirements.txt')
        local('pip download -r requirements.txt -d vendor --no-binary :all:')

        print('deps vendored')

        print('deploying to cloudfront')

        local('cf push')

        print('deployed')

    finally:

        print('reinstalling uninstalled packages')

        local('pipenv install -d')
        local('python setup.py install')


@task
def test_readme_rst():
    """Test README.rst to ensure it will render correctly in warehouse."""
    local('python setup.py check -r -s')


@task
def clean_build():
    """Remove build artifacts."""
    local('rm -fr build/')
    local('rm -fr dist/')
    local('rm -rf .eggs/')
    local("find . -name '*.egg-info' -exec rm -fr {} +")
    local("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc():
    """Remove Python file artifacts."""
    local("find . -name '*.pyc' -exec rm -f {} +")
    local("find . -name '*.pyo' -exec rm -f {} +")
    local("find . -name '*~' -exec rm -f {} +")
    local("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_test():
    """Remove test and coverage artifacts."""
    local('rm -fr .tox/')
    local('rm -f .coverage')
    local('rm -fr htmlcov/')


@task
def clean():
    """Remove all build, test, coverage and Python artifacts."""
    clean_build()
    clean_pyc()
    clean_test()


@task
def test(capture=True, pdb=False):
    """
    Run tests quickly with default Python.

    Args:
        capture: capture stdout [default: True]
        pdb: run debugger upon encountering exception
    """
    flags = ' '.join([
        '-s' if not true(capture) else '',
        '--pdb' if true(pdb) else ''
    ])
    local('py.test tests/' + ' ' + flags)


@task(alias='tox')
def test_all(absolute_path=None):
    """Run on multiple Python versions with tox."""
    local('tox')


@task
def coverage(open_browser=True):
    """Check code coverage quickly with the default Python."""
    local('coverage run --source {{ cookiecutter.project_slug }} -m pytest')
    local('coverage report -m')
    local('coverage html')
    if true(open_browser):
        local('open htmlcov/index.html')


@task
def docs(open_browser=True):
    """
    Generage Sphinx HTML documentation, including API docs.

    Args:
        open_browser: Open browser automatically after building docs
    """
    local('rm -f docs/{{ cookiecutter.project_slug }}.rst')
    local('rm -f docs/modules.rst')
    local('rm -f docs/{{ cookiecutter.project_slug }}*')
    local('sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}')

    with lcd('docs'):
        local('make clean')
        local('make html')

    local('cp -rf docs/_build/html/ public/')

    if true(open_browser):
        local('open public/index.html')

{% if cookiecutter.open_source == 'y' %}
@task
def publish_docs():
    """
    Compile docs and publish to GitHub Pages.

    Logic borrowed from `hugo <https://gohugo.io/tutorials/github-pages-blog/>`
    """
    from textwrap import dedent

    with settings(warn_only=True):
        if local('git diff-index --quiet HEAD --').failed:
            local('git status')
            abort('The working directory is dirty. Please commit any pending changes.')

        if local('git show-ref refs/heads/gh-pages').failed:
            # initialized github pages branch
            local(dedent("""
                git checkout --orphan gh-pages
                git reset --hard
                git commit --allow-empty -m "Initializing gh-pages branch"
                git push gh-pages
                git checkout master
                """).strip())
            print('created github pages branch')

    # deleting old publication
    local('rm -rf public')
    local('mkdir public')
    local('git worktree prune')
    local('rm -rf .git/worktrees/public/')
    # checkout out gh-pages branch into public
    local('git worktree add -B gh-pages public gh-pages')
    # generating docs
    docs(open_browser=False)
    # push to github
    with lcd('public'), settings(warn_only=True):
        local('git add .')
        local('git commit -m "Publishing to gh-pages (Fabfile)"')
        local('git push origin gh-pages')
{% endif %}

@task
def dist():
    """Build source and wheel package."""
    clean()
    local('python setup.py sdist')
    local('python setup.py bdist_wheel')


@task
def release():
    """Package and upload a release to pypi."""
    test_readme_rst()
    clean()
    test_all()
    publish_docs()
    local('python setup.py sdist bdist_wheel')
    local('twine upload dist/*')


@singledispatch
def true(arg):
    """
    Determine of the argument is True.

    Since arguments coming from the command line
    will always be interpreted as strings by fabric
    this helper function just helps us to do what is
    expected when arguments are passed to functions
    explicitly in code vs from user input.

    Just make sure NOT to do the following with task arguments:

    @task
    def foo(arg):
        if arg: ...

    Always wrap the conditional as so

    @task
    def foo(arg):
        if true(arg): ...

    and be aware that true('false') -> False

    Args:
        arg: anything

    Returns: bool

    """
    return bool(arg)


@true.register(str)
def _(arg):
    """If the lowercase string is 't' or 'true', return True else False."""
    argument = arg.lower().strip()
    return argument == 'true' or argument == 't'


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
