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

## Section 1: importing modules
import os
from pathlib import Path

from shapelets.astronomy.galaxy import load_fits_data, get_postage_stamps, decompose_galaxies

## Section 2: parameters
fits_name = "galaxies.fits"
shapelet_order = 10
compression_order = 20

## Section 3: code

# 3.1: loading .fits data and output directory handling
save_path = os.path.join(Path(__file__).parents[0], 'output')
if not os.path.exists(save_path): 
    os.mkdir(save_path)
fits_path = os.path.join(Path(__file__).parents[0], 'images', fits_name) 

output_base_path = save_path+fits_path[fits_path.rfind('/'):-5]
fits_data = load_fits_data(fits_path)

# 3.2 iidentifying areas in the image that contain decomposable galaxies
(galaxy_stamps, star_stamps, noiseless_data) = get_postage_stamps(fits_data, output_base_path)

# 3.3 starting with the biggest galaxy, decomposes subdomain into a collection of shapelet coefficients
decompose_galaxies(galaxy_stamps, star_stamps, noiseless_data, shapelet_order, compression_order, output_base_path)