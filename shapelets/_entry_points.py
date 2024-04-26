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
import platform
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
    time.sleep(10)
    
    # navigate to tests/ folder relative to this file
    tests_dir = os.path.join(Path(__file__).parents[0], 'tests')
    os.chdir(tests_dir)

    # automatically find all tests using unittest built-in discovery component
    # run unit tests from command line
    if str(platform.system()) == 'Windows':
        # force Python3, but specific version is difficult to automate
        os.system('py -3 -B -m unittest -v')
    
    else: # MAC and Linux systems
        # find specific python version based on installation path
        split_path = os.getcwd().split('/')
        py_version = [py for py in split_path if 'python' in py]
        if not py_version: # empty = default installation path not used, resort to default
            os.system('python3 -B -m unittest -v')
        else:
            # In the event of non-standard installation paths, take last entry in py_version
            os.system(f'{py_version[-1]} -B -m unittest -v')               