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

from . import _run

def _run_shapelets():
    r"""
    Main function that runs shapelets. This is only invoked via the entry point "shapelets CONFIG" where CONFIG is the name of the configuration plaintext file that exists in the same directory level as the working directory.  

    """
    # if user did not provide any configuration filename (which is required)
    if len(sys.argv) == 1: 
        raise RuntimeError('Please provide name of config file, i.e. "shapelets config".')

     # if user did provide a configuration filename/path
    elif len(sys.argv) == 2:
        config_file = sys.argv[1]
        working_dir = os.getcwd() 
        
        _run._run(config_file, working_dir)

    # if the user provides more than 1 argument (in addition to shapelets). Print error messages and quit.
    else: 
        raise RuntimeError('Please provide one argument (configuration filename), i.e.: "shapelets config".')


def _run_tests():
    r"""
    Main function that runs all the unit tests via unittest from Python STL. This is only invoked via the entry point "shapelets-test".
    
    """
    # notify user tests may take more than a few seconds
    print("Initiating shapelets unit tests. This will likely take a few minutes.")

    time.sleep(5)

    # if the user knows what they're doing, this would use same interpreter as that to install the package
    pyinterp = sys.executable 
    tests_dir = os.path.join(Path(__file__).parents[0], 'tests')

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
