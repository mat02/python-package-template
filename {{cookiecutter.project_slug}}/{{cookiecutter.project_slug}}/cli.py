"""{{ cookiecutter.project_slug }} v{{ cookiecutter.version }}

{{ cookiecutter.project_short_description }}

Usage:
    {{cookiecutter.project_slug }} [options] <argument>
    {{cookiecutter.project_slug }} -h | --help
    {{cookiecutter.project_slug }} -V | --version

Options:
    -h --help                 show help and exit
    -V --version              show version and exit
"""
from docopt import docopt


def main(argv=None):
    args = docopt(__doc__, argv=argv, version='{{ cookiecutter.version }}')
    print(args)

if __name__ == "__main__":
    main()
