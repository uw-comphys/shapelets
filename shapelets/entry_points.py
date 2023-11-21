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

import contextlib
import os
import platform
import sys 
from .run import *

def run_shapelets():
    r""" 
    
    Main function that runs shapelets.
    This is only invoked via the entry point "shapelets".
    I.e., in a directory with a configuration plaintext file, you should enter "shapelets filename" where
        'filename' is the name of the configuration plaintext file via the CLI (command line interface).

    Args (from command line):
        config_file: Filename of the config file to load. Required parameter.

    """
    
    # Arguments for command line use
    if len(sys.argv) == 1: # if user did not provide any configuration path (which is required)
        raise RuntimeError("ERROR: Please provide configuration file.")

    elif len(sys.argv) == 2: # if user did provide a configuration path
        config_file = sys.argv[1]
        run(config_file)

    else: # if the user provides more than 1 argument (in addition to opencmp). Print error messages and quit.
        raise RuntimeError("Improper use of shapelets module. Try 'shapelets config' with config file present.")

def run_tests():
    r"""
    
    Main function that runs all the unit tests via unittest from Python STL.
    This is only invoked via the entry point "shapelets-test" from the topmost shapelets directory.
    I.e., only from the directory "/.../shapelets/" should you enter "shapelets-test" via the CLI 
        (command line interface).
    
    """

    @contextlib.contextmanager
    def tempWorkingDir(path):
        r"""
        
        Temporarily create a working directory to execute CLI commands without actually
        changing the root of the global directory.

        From stackoverflow here:
        https://stackoverflow.com/questions/75048986/way-to-temporarily-change-the-directory-in-python-to-execute-code-without-affect
        
        """
        oldir = os.getcwd()
        os.chdir(os.path.abspath(path))
        try: yield
        finally: os.chdir(oldir)

    # get platform and then assume entry point "testshapelets" executed from top-level directory
    user_os = str(platform.system())
    if user_os == 'Windows':
        os.chdir("tests\\")
        runcom = "python -B -m"
    else:
        os.chdir("tests/")
        runcom = "python3 -B -m"

    # find all .py files nested in tests/, and run them sequentially
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                with tempWorkingDir(root):
                    print(f"\n\nRunning tests in {file}")
                    if user_os == 'Windows': os.system(f"{runcom} {file}")
                    else: os.system(f"{runcom} {file[:-3]}")                    
