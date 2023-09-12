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

from shapelets.self_assembly import (
    convresponse,
    read_image,
    rdistance,
    get_wavelength,
    process_output
) 

## Section 2: parameters
image_name = "lamSIM1.png"
shapelet_order = 'default' 
num_clusters = 20
ux = [50, 80]
uy = [150, 180]

## Section 3: code

# 3.1: image and output directory handling
image_path = os.getcwd()+'/images/'
image = read_image(image_name = image_name, image_path = image_path)
save_path = os.getcwd()+'/output/'
if not os.path.exists(save_path): os.mkdir("output")

# 3.2: get the characteristic wavelength of the pattern
char_wavelength = get_wavelength(image = image)

# 3.3: get the convolutional response 
response = convresponse(image = image, l = char_wavelength, shapelet_order = shapelet_order, normresponse = 'Vector')[0]

# 3.4: compute the response distance 
try:
    rd_field = rdistance(image = image, response = response, num_clusters = num_clusters, ux = ux, uy = uy)
except NameError:
    rd_field = rdistance(image = image, response = response, num_clusters = num_clusters, ux = 'default', uy = 'default')

# processing and saving the results to the **output/** directory 
process_output(image = image, image_name = image_name, save_path = save_path, output_from = 'response_distance', d = rd_field, num_clusters = num_clusters)
