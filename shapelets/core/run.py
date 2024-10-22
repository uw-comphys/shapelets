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

import configparser
import os

from .analysis import do_analysis, METHODS_ASTRONOMY, METHODS_SELFASSEMBLY

def run(config_file: str, working_dir: str) -> None:
    r"""
    Main run function that parses the configuration file, ensures it exists in the provided (working) directory, and sets up output directory for post-analysis.
    
    Parameters
    ----------
    * config_file : str
        * The name of the configuration file in working_dir
    * working_dir : str
        * The absolute path (working directory) where the entry point was invoked from

    """
    config = configparser.ConfigParser()

    config_file = os.path.join(working_dir, config_file)

    if not os.path.exists(config_file):
        raise RuntimeError(f"Configuration file {config_file} does not exist. Check filename spelling and ensure it is located in {working_dir}.")

    config.read(config_file)

    all_methods = METHODS_ASTRONOMY + METHODS_SELFASSEMBLY

    if config.get('general', 'method') not in all_methods:
        raise RuntimeError(f"The method '{config.get('general', 'method')}' provided in configuration file '{config_file}' is not recognized by shapelets. Available options are: {', '.join(m for m in all_methods)}.")
    
    image_dir = os.path.join(working_dir, 'images')
    if not os.path.exists(image_dir): 
        raise RuntimeError(f"Path '{image_dir}' does not exist.")
    
    output_dir = os.path.join(working_dir, 'output')
    if not os.path.exists(output_dir): 
        os.mkdir(output_dir)

    do_analysis(config, working_dir, image_dir, output_dir)