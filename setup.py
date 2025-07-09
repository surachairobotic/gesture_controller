# ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# This function reads information from your package.xml and uses it to
# generate arguments for the setup() function.
setup_args = generate_distutils_setup(
    packages=[], # We have no python modules in this package, only scripts
    package_dir={'': 'src'}
)

setup(**setup_args)
