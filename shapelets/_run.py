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

import ast
import configparser
import os
from pathlib import Path

from .astronomy.galaxy import *

from .self_assembly.misc import *
from .self_assembly.quant import *
from .self_assembly.wavelength import *

def _run(config_file: str, working_dir: str) -> None:
    r"""
    Main run function that handles input configuration file.
    
    Parameters
    ----------
    * config_file : str
        * The name of the configuration file in working_dir
    * working_dir : str
        * The absolute path (working directory) where the entry point was invoked from
    
    Notes
    -----
    Differentiation between submodule use is based on image_name or fits_name provided in config file. Note that this may need to be changed in the future if more astronomy functionality is added.

    """
    ## configparser setup and input/output path organization ##

    # instantiate and read
    config = configparser.ConfigParser()
    config_file = os.path.join(working_dir, config_file)
    if not os.path.exists(config_file):
        raise RuntimeError(f"Configuration file {config_file} does not exist. Check config filename spelling and ensure that it is located in {working_dir}.")
    else:
        config.read(config_file)

    # handle method
    method = config.get('general', 'method')

    # image and output paths
    image_path = os.path.join(working_dir, 'images')
    save_path = os.path.join(working_dir, 'output')
    if not os.path.exists(image_path): 
        raise RuntimeError(f"Path '{image_path}' does not exist.")
    if not os.path.exists(save_path): 
        os.mkdir(save_path)

    ## self_assembly submodule use ##
        
    # parsing input image of nanostructure
    if config.get('general', 'image_name', fallback=None):

        # read image to be analyzed
        image_name = config.get('general', 'image_name')
        image = read_image(image_name = image_name, image_path = image_path)

        # obtain characteristic wavelength, needed for all self-assembly applications
        char_wavelength = get_wavelength(image = image)

        if method == 'response_distance':
            shapelet_order = config.get('response_distance', 'shapelet_order', fallback = 'default')
            if shapelet_order != 'default':
                shapelet_order = ast.literal_eval(shapelet_order)

            num_clusters = config.get('response_distance', 'num_clusters', fallback = 'default')
            if num_clusters != 'default':
                num_clusters = ast.literal_eval(num_clusters)

            ux = config.get('response_distance', 'ux', fallback = 'default')
            uy = config.get('response_distance', 'uy', fallback = 'default')
            if ux != 'default':
                ux = ast.literal_eval(ux)
            if uy != 'default':
                uy = ast.literal_eval(uy)

            rd_field = rdistance(image = image, num_clusters = num_clusters, shapelet_order = shapelet_order, ux = ux, uy = uy)
            process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'response_distance', d = rd_field, num_clusters = num_clusters)

        elif method == 'orientation':
            pattern_order = config.get('orientation', 'pattern_order')

            response, orients = convresponse(image = image, l = char_wavelength, shapelet_order = 6, normresponse = 'Individual')
            mask, dilate, blended, maxval = orientation(pattern_order = pattern_order, l = char_wavelength, response = response, orients = orients)
            process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'orientation', mask = mask, dilate = dilate, orientation = blended, maxval = maxval)
    
        elif method == 'identify_defects':
            pattern_order = config.get('identify_defects', 'pattern_order')

            num_clusters = config.get('identify_defects', 'num_clusters', fallback = 'default') 
            if num_clusters != 'default':
                num_clusters = ast.literal_eval(num_clusters)

            response = convresponse(image = image, l = char_wavelength, shapelet_order = 'default', normresponse = 'Vector')[0]
            centroids, clusterMembers, defects = defectid(response = response, l = char_wavelength,
                                                          pattern_order = pattern_order, num_clusters = num_clusters)
            process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'identify_defects', centroids = centroids, clusterMembers = clusterMembers, defects = defects)
        
        else:
            raise ValueError('"method" parameter from configuration file not recognized by shapelets.')

    ## astronomy submodule use ##
        
    # retrieving .fits path (if .fits file is provided)
    elif config.get('general', 'fits_name', fallback=None):
        fits_path = os.path.join(working_dir, 'images', config.get('general', 'fits_name'))

        if method == 'galaxy_decompose':
            shapelet_order = config.get('galaxy_decompose', 'shapelet_order', fallback = 'default')
            compression_order = config.get('galaxy_decompose', 'compression_order', fallback = 'default')

            output_base_path = save_path+fits_path[fits_path.rfind('/'):-5]
            n_max = int([shapelet_order, 10][shapelet_order == 'default'])
            compression_factor = int([compression_order, 25][compression_order == 'default'])

            fits_data = load_fits_data(fits_path)
            (galaxy_stamps, star_stamps, noiseless_data) = get_postage_stamps(fits_data, output_base_path)
            decompose_galaxies(galaxy_stamps, star_stamps, noiseless_data, n_max, compression_factor, output_base_path)

        else:
            raise ValueError('"method" parameter from configuration file not recognized by shapelets.')
        
    else:
        raise NameError('No image (from image_name) or FITS (from fits_name) listed in configuration file.')