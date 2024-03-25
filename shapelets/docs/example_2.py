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

r"""

# Example 2 - Defect Identification

See [here](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2) for example files and code. 

This example demonstrates the defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) for self-assembly microscopy imaging using the ``shapelets.self_assembly`` submodule.

This example can be run in two different ways:
* (1) text-based configuration files (shown here), and 
* (2) programmatically via script-based Python programming (`example_2.py`)

## Overview

The defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is a modification of the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)), whereby the user is required to manually select clusters associated with defects or defect structures, and the defect response distance is computed for each response vector in each cluster. 

The defect response distance is similar to the response distance, but the reference subdomain is the centroid response vector of each cluster (and not a set of reference response vectors). For example, for a given cluster $C$ with centroid $C_c$, the defect response distance for response vector $c_i$ belonging to cluster $C$ with centroid response vector $C_c$ is computed as:

$$ d_i = \| C_c - c_i \|_2 $$

The key observation is that cluster response vectors with larger defect response distances are more "defect-like", allowing use of the defect response distance as a quantitative measure of "defect intensity" ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)).

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2) should contain the following.

![](images/example_2_dir.png)

where **config** is the text-based configuration file, **example_2.py** is the Python script file, and **images/** holds the simulated hexagonal self-assembled nanostructure image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for analysis.

![](images/hexSIM1.png)

## Configuration File Method

### Setup

The configuration file provided in the example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1) contains the following information:

	[general]
	image_name = hexSIM1.png
	method = identify_defects

	[identify_defects]
	pattern_order = hexagonal
	num_clusters = 10

where **image_name** and **method** are required parameters that specify the image filename and method used for analysis.

The method outlined in the configuration file will also have its own header with specific parameters. The **identify_defects** method may contain up to two parameters. Note that default refers to the default value if the parameter is excluded from the configuration file.

**pattern_order** `str`

* The pattern order (symmetry) observed in the image. Options are `stripe`, `square`, `hexagonal`
* This parameter **does not have a default value**

**num_clusters** `int`

* The number of clusters for k-means clustering. Must be $\geq$ 1.
* Default values are as follows,
	* If pattern_order = stripe $\rightarrow$ 4
	* If pattern_order = square $\rightarrow$ 8
	* If pattern_order = hexagonal $\rightarrow$ 10
* If an integer value is provided that is below the above default, the code will defer to the default value

### Run Example

Please ensure that `shapelets` is properly installed before proceeding.
See [here](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html) for installation instructions.

Navigate your terminal to "shapelets/examples/example_2". When you are ready, execute ``shapelets config`` in the command line.

During runtime you will be prompted to manually select the clusters associated with defects or defect structures. Please follow these instructions and use

* ``a`` to select a cluster in no particular order (duplicates are handled appropriately, 
* ``backspace/delete`` to remove the most recently selected cluster, and 
* ``enter`` when you have finished selecting defect clusters

**Additional Tips**

* You may use the **magnifying glass** (bottom left) to zoom in on a specific region
* You may use the **left arrow** (bottom left) to return to original zoom

The output (shown below) will be available in "shapelets/examples/example_2/output" containing the location of each cluster (top left), radar chart of centroid response vectors (top right), the defect response distance scalar field (bottom left), and this field superimposed onto the original pattern (bottom right). In this example, clusters 2, 5, and 8 were chosen by the user as defect clusters. 

![](images/hexSIM1_defectid_clustloc_k10.png)
![](images/hexSIM1_defectid_rc_k10.png)

![](images/hexSIM1_defectid_drd_k10.png)
![](images/hexSIM1_defectid_drd_overlay_k10.png)

## Scripting Method

For users comfortable with Python programming, the example_2.py file is structured to run the same analysis as described previously. The outputs will appear in the same directory.

"""
