########################################################################################################################
# Copyright 2023 the authors (see AUTHORS file for full list).                                                         #
#                                                                                                                      #
# This file is part of shapelets.                                                                                      #
#                                                                                                                      #
# Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General       #
# Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)  #
# any later version.                                                                                                   #
#                                                                                                                      #
# Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied      #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see           #
# <https://www.gnu.org/licenses/>.                                                                                     #
########################################################################################################################

import os
from pathlib import Path
import subprocess
import sys 
import time

from . import run

def run_shapelets():
    r"""
    Main function that runs shapelets that is called via entry point "shapelets-run".
    Currently supports one additional argument - the path to configuration file. 
    Example - "shapelets-run /path/to/CONFIG" where /path/to/CONFIG is the relative or absolute path to a configuration file.
    """
    # enforce configuration filepath
    if len(sys.argv) == 2: 
        working_dir = os.getcwd()
        config_filepath = sys.argv[1]

        # ensure configuration file exists
        if not os.path.isabs(config_filepath):
            config_filepath = os.path.join(working_dir, config_filepath)
        if not os.path.isfile(config_filepath):
            raise RuntimeError(f'Configuration file at {config_filepath} was not found.')
        
        # change working directory to where config is stored
        working_dir = Path(config_filepath).parents[0]
        os.chdir(working_dir)

        run.run(config_filepath, working_dir)
    else: 
        raise RuntimeError('Please provide the path to the configuration file, i.e. "shapelets-run /path/to/config".')


def run_tests():
    r"""
    Main function that runs all the unit tests via unittest from Python STL. This is only invoked via the entry point "shapelets-test" from any directory on your system.
    """
    print("Initiating shapelets unit tests. This will likely take a few minutes.")

    time.sleep(3)

    # if the user knows what they're doing, this would use same interpreter as that to install the package
    pyinterp = sys.executable 
    tests_dir = os.path.join(Path(__file__).parents[1], 'tests')

    # automatically find and run all unit tests using unittest built-in discovery feature
    if pyinterp:
        subprocess.call([pyinterp, '-B', '-m', 'unittest', '-v'], cwd=tests_dir)

    else: 
        # This loop should theoretically never hit... an interpreter should always be found
        import platform
        ostype = str(platform.platform())

        print('Do you have a regular Python interpreter installed on your machine?')
        print('Attempting manual unit testing...')

        if 'win' in ostype.lower():
            subprocess.call(['py', '-3', '-B', '-m', 'unittest', '-v'], cwd=tests_dir)
        else:
            subprocess.call(['python3', '-B', '-m', 'unittest', '-v'], cwd=tests_dir)
