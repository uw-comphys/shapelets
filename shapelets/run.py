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

from shapelets.astronomy.galaxy import decompose_galaxies, get_postage_stamps, load_fits_data
from shapelets.self_assembly.misc import process_output, read_image
from shapelets.self_assembly.apps import identify_defects, orientation, response_distance

METHODS = [
    'galaxy_decompose',
    'response_distance', 
    'orientation', 
    'identify_defects'
]


def run(
    config_filepath: str, 
    working_dir: str
):
    r""" Main run function that does the following,
        (1) parses the configuration file, 
        (2) sets up output directory for results, and 
        (3) runs associated analysis, saving results

    Parameters
    ----------
    config_filepath : str
        The absolute or relative path of a configuration file
    working_dir : str
        The working directory (where the config. file is) 

    """
    config = configparser.ConfigParser()
    config.read(config_filepath)

    if config.get('general', 'method') not in METHODS:
        available_methods = ', '.join(m for m in METHODS)
        errmsg  = f"The method '{config.get('general', 'method')}' in configuration your file is invalid.\n"
        errmsg += f"Available options are {available_methods}" 
        raise RuntimeError(errmsg)
    
    image_dir = os.path.join(working_dir, 'images')
    if not os.path.exists(image_dir): 
        errmsg = f"Path '{image_dir}' does not exist."
        raise RuntimeError(errmsg)
    
    output_dir = os.path.join(working_dir, 'output')
    if not os.path.exists(output_dir): 
        os.mkdir(output_dir)

    # Grab method that user wants to run
    method = config.get('general', 'method')

    # ------------------- #
    # shapelets.astronomy #
    # ------------------- #

    if method == 'galaxy_decompose':
        fits_name = config.get('general', 'fits_name')
        fits_path = os.path.join(working_dir, 'images', fits_name)

        shapelet_order = config.get('galaxy_decompose', 'shapelet_order', fallback = 'default')
        compression_order = config.get('galaxy_decompose', 'compression_order', fallback = 'default')

        output_base_path = output_dir+fits_path[fits_path.rfind('/'):-5]
        n_max = int([shapelet_order, 10][shapelet_order == 'default'])
        compression_factor = int([compression_order, 25][compression_order == 'default'])

        fits_data = load_fits_data(fits_path)
        (galaxy_stamps, star_stamps, noiseless_data) = get_postage_stamps(fits_data, output_base_path)
        decompose_galaxies(galaxy_stamps, star_stamps, noiseless_data, n_max, compression_factor, output_base_path)

        return

    # ----------------------- #
    # shapelets.self_assembly #
    # ----------------------- #

    image_name = config.get('general', 'image_name')
    image = read_image(image_name = image_name, image_path = image_dir)

    if method == 'response_distance':
        shapelet_order = config.get(
            'response_distance', 
            'shapelet_order', 
            fallback = 'default'
        )

        if shapelet_order != 'default':
            shapelet_order = ast.literal_eval(shapelet_order)

        num_clusters = config.get('response_distance', 'num_clusters', fallback = 20)
        num_clusters = ast.literal_eval(num_clusters)

        ux = config.get('response_distance', 'ux', fallback = 'default')
        uy = config.get('response_distance', 'uy', fallback = 'default')
        if ux != 'default':
            ux = ast.literal_eval(ux)
        if uy != 'default':
            uy = ast.literal_eval(uy)

        rd_field = response_distance(
            image = image, 
            num_clusters = num_clusters, 
            shapelet_order = shapelet_order, 
            ux = ux, 
            uy = uy
        )

        output_objects = (rd_field, num_clusters)

    elif method == 'orientation':
        pattern_order = config.get(
            'orientation', 
            'pattern_order'
        )

        mask, dilate, blended, maxval = orientation(
            image = image, 
            pattern_order = pattern_order
        )

        output_objects = (mask, dilate, blended, maxval)

    elif method == 'identify_defects':
        pattern_order = config.get(
            'identify_defects', 
            'pattern_order'
        )

        centroids, clusterMembers, defects = identify_defects(image = image, pattern_order = pattern_order)

        output_objects = (centroids, clusterMembers, defects)

    # save outputs
    process_output(
        image = image, 
        image_name = image_name, 
        save_path = output_dir, 
        output_from = method, 
        output_objects = output_objects,
    )

    return