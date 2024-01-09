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

from .self_assembly.misc import *
from .self_assembly.quant import *
from .self_assembly.wavelength import *

from .astronomy.galaxy import *

def run(config_file: str) -> None:
    r""" 
    
    Main run function that handles input configuration file.
    
    Parameters
    ----------

    config_file : str
        The name of the config file.
    """

    # instance and read
    config = configparser.ConfigParser()
    config.read(config_file)

    # handle method
    method = config.get('general', 'method')

    # image and output paths
    image_path = os.getcwd()+'/images/'
    save_path = os.getcwd()+'/output/'
    if not os.path.exists(image_path): 
        raise RuntimeError(f"Path '{image_path}' does not exist.")
    if not os.path.exists(save_path): 
        os.mkdir("output")

    # parsing image
    if config.get('general', 'image_name', fallback=None):
        image_name = config.get('general', 'image_name')
        image = read_image(image_name = image_name, image_path = image_path)
    if config.get('general', 'image_name', fallback=None):
        image_name = config.get('general', 'image_name')
        image = read_image(image_name = image_name, image_path = image_path)

        # obtain characteristic wavelength, needed for all self-assembly applications
        char_wavelength = get_wavelength(image = image)
        # obtain characteristic wavelength, needed for all self-assembly applications
        char_wavelength = get_wavelength(image = image)

    # retrieving .fits path (if .fits file is provided)
    if config.get('general', 'fits_name', fallback=None):
        fits_path = os.getcwd()+'/images/' + config.get('general', 'fits_name')
    # retrieving .fits path (if .fits file is provided)
    if config.get('general', 'fits_name', fallback=None):
        fits_path = os.getcwd()+'/images/' + config.get('general', 'fits_name')

    ## response_distance
    if method == 'response_distance':
        shapelet_order = config.get('response_distance', 'shapelet_order', fallback = 'default')
        num_clusters = config.get('response_distance', 'num_clusters', fallback = 'default')
        ux = config.get('response_distance', 'ux', fallback = 'default')
        uy = config.get('response_distance', 'uy', fallback = 'default')
        # if ux/uy are a list (but read by configparser as a str), then convert to list)
        if ux != 'default':
            ux = ast.literal_eval(ux)
        if uy != 'default':
            uy = ast.literal_eval(uy)

        response = convresponse(image = image, l = char_wavelength, shapelet_order = shapelet_order, normresponse = 'Vector')[0]
        rd_field = rdistance(image = image, response = response, num_clusters = num_clusters, ux = ux, uy = uy)

        process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'response_distance', \
                       d = rd_field, num_clusters = num_clusters)

    ## orientation
    elif method == 'orientation':
        pattern_order = config.get('orientation', 'pattern_order')

        response, orients = convresponse(image = image, l = char_wavelength, shapelet_order = 6, normresponse = 'Individual')
        mask, dilate, blended, maxval = orientation(pattern_order = pattern_order, l = char_wavelength, \
                                                    response = response, orients = orients)

        process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'orientation', \
                       mask = mask, dilate = dilate, orientation = blended, maxval = maxval)
  
    ## defectid
    elif method == 'identify_defects':
        pattern_order = config.get('identify_defects', 'pattern_order')
        num_clusters = config.get('identify_defects', 'num_clusters', fallback = 'default')

        response = convresponse(image = image, l = char_wavelength, shapelet_order = 'default', normresponse = 'Vector')[0]
        centroids, clusterMembers, defects = defectid(response = response, l = char_wavelength, \
                                                      pattern_order = pattern_order, num_clusters = num_clusters)

        process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'identify_defects', \
                       centroids = centroids, clusterMembers = clusterMembers, defects = defects)

    #galaxy_decomposition
    elif method == 'galaxy_decompose':
        shapelet_order = config.get('galaxy_decompose', 'shapelet_order', fallback = 'default')
        compression_order = config.get('galaxy_decompose', 'compression_order', fallback = 'default')

        output_base_path = save_path+fits_path[fits_path.rfind('/'):-5]
        n_max = int([shapelet_order, 10][shapelet_order == 'default'])
        compression_factor = int([compression_order, 25][compression_order == 'default'])

        fits_data = load_fits_data(fits_path)
        (galaxy_stamps, star_stamps, noiseless_data) = get_postage_stamps(fits_data, output_base_path)
        decompose_galaxies(galaxy_stamps, star_stamps, noiseless_data, n_max, compression_factor, output_base_path)