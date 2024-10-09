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
import sys

from ..astronomy.galaxy import decompose_galaxies, get_postage_stamps, load_fits_data
from ..self_assembly.misc import process_output, read_image
from ..self_assembly.quant import defectid, orientation, rdistance

METHODS_ASTRONOMY       = ['galaxy_decompose']
METHODS_SELFASSEMBLY    = ['response_distance', 'orientation', 'identify_defects']

def do_analysis(config: configparser.ConfigParser, working_dir: str, image_dir: str, output_dir: str) -> None:
    r"""
    Main function that handles usage of the configuration file method by appropriately directing the parameters in the config file for the requested analysis.

    Parameters
    ----------
    * config : configparser.ConfigParser
        * The parsed configuration file
    * working_dir : str 
        * The absolute path (working directory) where the entry point was invoked from
    * image_dir : str
        * The directory containing the image (or .FITS file) for analysis
    * output_dir : str
        * The output directory where results from the analysis will be saved

    """
    method = config.get('general', 'method')

    # shapelets.astronomy submodule #
    # ----------------------------- #

    # galaxy decomposition: https://doi.org/10.1046/j.1365-8711.2003.05901.x
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

        sys.exit()


    # shapelets.self_assembly #
    # ----------------------- #

    image_name = config.get('general', 'image_name')
    image = read_image(image_name = image_name, image_path = image_dir)

    # response distance: https://doi.org/10.1088/1361-6528/ad1df4
    if method == 'response_distance':
        shapelet_order = config.get('response_distance', 'shapelet_order', fallback = 'default')
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

        rd_field = rdistance(image = image, num_clusters = num_clusters, shapelet_order = shapelet_order, ux = ux, uy = uy)

        process_output(image = image, image_name = image_name, save_path = output_dir, output_from = 'response_distance', d = rd_field, num_clusters = num_clusters)

    # local pattern orientation: https://doi.org/10.1088/1361-6528/ad1df4
    elif method == 'orientation':
        pattern_order = config.get('orientation', 'pattern_order')

        mask, dilate, blended, maxval = orientation(image = image, pattern_order = pattern_order)

        process_output(image = image, image_name = image_name, save_path = output_dir, output_from = 'orientation', mask = mask, dilate = dilate, orientation = blended, maxval = maxval)
    
    # defect identification method: https://doi.org/10.1088/1361-6528/ad1df4
    elif method == 'identify_defects':
        pattern_order = config.get('identify_defects', 'pattern_order')

        centroids, clusterMembers, defects = defectid(image = image, pattern_order = pattern_order)

        process_output(image = image, image_name = image_name, save_path = output_dir, output_from = 'identify_defects', centroids = centroids, clusterMembers = clusterMembers, defects = defects)