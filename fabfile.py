from fabric.api import *

@task
def gen_requirements_txt():
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
    for item in pip_config.items('packages'):
        lib, version = item
        lib, version = lib.strip('"'), version.strip('"')
        # ungracefully handle wildcard requirements
        if version == '*': version = ''
        packages.append(lib + version)

    requirements_file.write_text('\n'.join(packages))
    print('successfully generated requirements.txt')
