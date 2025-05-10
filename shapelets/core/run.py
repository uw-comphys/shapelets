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

def run(config_filepath: str, working_dir: str) -> None:
    r"""
    Main run function that 
        (1) parses the configuration file, 
        (2) sets up output directory for results, and 
        (3) runs associated analysis

    Parameters
    ----------
    * config_filepath : str
        * The absolute or relative path of a configuration file
    * working_dir : str
        * The working directory which is where the configuration file is stored

    """
    config = configparser.ConfigParser()
    config.read(config_filepath)

    all_methods = METHODS_ASTRONOMY + METHODS_SELFASSEMBLY
    if config.get('general', 'method') not in all_methods:
        available_methods = ', '.join(m for m in all_methods)
        raise RuntimeError(f"The method '{config.get('general', 'method')}' provided in configuration your file is invalid. Available options are: {available_methods}.")
    
    image_dir = os.path.join(working_dir, 'images')
    if not os.path.exists(image_dir): 
        raise RuntimeError(f"Path '{image_dir}' does not exist.")
    
    output_dir = os.path.join(working_dir, 'output')
    if not os.path.exists(output_dir): 
        os.mkdir(output_dir)

    do_analysis(config, working_dir, image_dir, output_dir)