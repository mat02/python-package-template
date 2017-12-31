import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
PACKAGE_REGEX = r'^[a-z][a-z0-9-]+$'

module_name = '{{ cookiecutter.project_slug }}'
package_name ='{{ cookiecutter.package_name }}'

if not re.match(PACKAGE_REGEX, package_name):
    print('ERROR: {} is not a valid name for a package. Please refer to PEP 8 and avoid uppercase letters and underscores'.format(package_name))
elif not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    #Exit to cancel project
    sys.exit(1)
