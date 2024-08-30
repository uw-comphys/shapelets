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

from shapelets.self_assembly import (
    read_image,
    rdistance,
    process_output
) 

## Section 2: parameters
image_name = "lamSIM1.png"
shapelet_order = 'default' # can also be integer value to set upper bound
num_clusters = 'default' # default is 20, can be any other positive integer 
ux = [109, 158]
uy = [283, 322]

## Section 3: code

# 3.1: image and output directory handling
image_path = os.path.join(Path(__file__).parents[0], 'images')
image = read_image(image_name = image_name, image_path = image_path)
save_path = os.path.join(Path(__file__).parents[0], 'output')
if not os.path.exists(save_path): 
    os.mkdir(save_path)

# 3.2: compute the response distance 
try: # if ux, uy are defined above
    rd_field = rdistance(image = image, num_clusters = num_clusters, shapelet_order = shapelet_order, ux = ux, uy = uy)
except NameError:
    rd_field = rdistance(image = image, num_clusters = num_clusters, shapelet_order = shapelet_order, ux = 'default', uy = 'default')

# 3.3: processing and saving the results to the **output/** directory 
process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'response_distance', d = rd_field, num_clusters = num_clusters)
