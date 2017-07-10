from functools import singledispatch

from fabric.api import *


@task
def gen_requirements_txt(with_dev=True):
    """
    Generate a requirements.txt from Fabfile.

    This is more for the benefit of third-party packages
    like pyup.io that need requirements.txt
    """
    from configparser import ConfigParser
    from pathlib import Path

    pip_config = ConfigParser()
    pip_config.read('Pipfile')
    requirements_file = Path('requirements.txt')
    packages = []
    items = pip_config.items('packages')
    if true(with_dev) and pip_config.has_section('dev-packages'):
        items.extend(pip_config.items('dev-packages'))
    for item in items:
        lib, version = item
        lib, version = lib.strip('"'), version.strip('"')
        # ungracefully handle wildcard requirements
        if version == '*': version = ''
        packages.append(lib + version)

    requirements_file.write_text('\n'.join(packages))
    print('successfully generated requirements.txt')


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
