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

# Examples Overview

The files and code associated with these examples can be found in the [github example directory](https://github.com/uw-comphys/shapelets/tree/main/examples). 

## Example 1 - Response Distance

This example goes demonstrates the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for self-assembly microscopy imaging using the ``shapelets.self_assembly`` submodule.

This example can be run in two different ways:
* (1) text-based configuration files (shown here), and 
* (2) programmatically via script-based Python programming (`example_1.py`)

### Overview

The response distance ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) is calculated as:

$$ d_{i, j} = \min \| \vec{R} - \vec{r_{i,j}} \|_2 $$

where $\vec{r_{i,j}}$ denotes the given response vector at pixel location $\{i, j\}$ and $\vec{R}$ is the reference set (or subdomain) of response vectors.

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1) should contain the following.

![](images/example_1_dir.png)

where **config** is the text-based configuration file, **example_1.py** is the Python script file, and **images/** holds the simulated stripe self-assembled nanostructure image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for analysis.

![](images/lamSIM1.png)

### Configuration File Method - Setup

The configuration file provided in the example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1) contains the following information:

	[general]
	image_name = lamSIM1.png
	method = response_distance

	[response_distance]
	shapelet_order = default
	num_clusters = 20
	ux = [50, 80]
	uy = [150, 180]

where **image_name** and **method** are required parameters that specify the image filename and method used for analysis.

The method outlined in the configuration file will also have its own header with specific parameters. The **response_distance** method may contain up to four parameters. Note that *default* refers to the default value if the parameter is excluded from the configuration file.

**shapelet_order** `int`

* The maximum shapelet order ($m'$) used for convolution operations, i.e. $m \in [1, m']$ shapelets are used 
* default = $m'$ $\rightarrow$ computed by the higher-order shapelet algorithm ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4))

**num_clusters** `int`

* The number of clusters for k-means clustering. Note using 0 is acceptable and will use all response vectors in the reference region (subdomain) ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307))
* default = 20 $\rightarrow$ as determined by a distortion analysis ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353))

**ux** `list`

* The lower and upper x-coordinates (respectively) of the reference region (subdomain)
* default $\rightarrow$ user is required to select x-bounds during runtime, see [here](#selecting-subdomain-bounds-during-runtime) for instructions

**uy** `list`

* The lower and upper y-coordinates (respectively) of the reference region (subdomain)
* default $\rightarrow$ user is required to select y-bounds during runtime, see [here](#selecting-subdomain-bounds-during-runtime) for instructions


### Configuration File Method - Run

Please ensure that `shapelets` is properly installed before proceeding.

Navigate your terminal to "shapelets/examples/example_1". When you are ready, execute ``shapelets config`` in the command line.

The output (shown below) will be available in "shapelets/examples/example_1/output" containing the response distance scalar field (left) as well as this field superimposed onto the original pattern (right).

![](images/lamSIM1_response_distance_k20.png)
![](images/lamSIM1_response_distance_overlay_k20.png)

### Scripting Method

For users comfortable with Python programming, the **example_1.py** file is structured to run the same analysis as described previously. The outputs will appear in the same directory.

### Selecting subdomain bounds during runtime

If you are computing the response distance method for the first time on a new image, you have the option to omit the **ux** and **uy** parameters so that you can choose the reference region during runtime. 

**Selecting bounds during runtime**

After executing example 1, either via ``shapelets config`` in the command line (Configuration File Method) or programmatically through **example_1.py**, you will be prompted to select four (4) points that represent the corners/bounds of the reference subdomain. At this point, you can use

* ``a`` to select a corner (bound) in no particular order, 
* ``backspace/delete`` to remove the most recently selected corner, and 
* ``enter`` when you have finished selecting 4 points/corners 

**Additional Tips**

* You may use the **magnifying glass** (bottom left) to zoom in on a specific region
* You may use the **left arrow** (bottom left) to return to original zoom
* Failure to choose 4 points/corners (i.e., choosing less or more than 4) will restart the process automatically
* Please choose a region of the pattern that contains zero observable defects in order to maximize the response distance results

## Example 2 - Defect Identification

This example demonstrates the defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) for self-assembly microscopy imaging using the ``shapelets.self_assembly`` submodule.

This example can be run in two different ways:
* (1) text-based configuration files (shown here), and 
* (2) programmatically via script-based Python programming (`example_2.py`)

### Overview

The defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is a modification of the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)), whereby the user is required to manually select clusters associated with defects or defect structures, and the defect response distance is computed for each response vector in each cluster. 

The defect response distance is similar to the response distance, but the reference subdomain is the centroid response vector of each cluster (and not a set of reference response vectors). For example, for a given cluster $C$ with centroid $C_c$, the defect response distance for response vector $c_i$ belonging to cluster $C$ with centroid response vector $C_c$ is computed as:

$$ d_i = \| C_c - c_i \|_2 $$

The key observation is that cluster response vectors with larger defect response distances are more "defect-like", allowing use of the defect response distance as a quantitative measure of "defect intensity" ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)).

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2) should contain the following.

![](images/example_2_dir.png)

where **config** is the text-based configuration file, **example_2.py** is the Python script file, and **images/** holds the simulated hexagonal self-assembled nanostructure image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for analysis.

![](images/hexSIM1.png)

### Configuration File Method - Setup

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

### Configuration File Method - Run

Please ensure that `shapelets` is properly installed before proceeding.

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

### Scripting Method

For users comfortable with Python programming, the example_2.py file is structured to run the same analysis as described previously. The outputs will appear in the same directory.

## Example 3 - Local Pattern Orientation

This example demonstrates computation of the local pattern orientation  for self-assembly microscopy imaging using the ``shapelets.self_assembly`` submodule.

This example can be run in two different ways:
* (1) text-based configuration files (shown here), and 
* (2) programmatically via script-based Python programming (`example_3.py`)

### Overview

Local pattern orientation is concerned with the relative orientation of nanostructure along grain boundaries and in between grains. The local pattern orientation method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) contains three (3) main steps:

* (1) **Masking**: Performed for well-defined features using a specific response threshold. This threshold is found via an interative scheme. Only the orientation values from these well-defined features are retained after masking.
* (2) **Dilation**: Performed via morphological greyscale dilation from ``scipy.ndimage.grey_dilation`` ([P. Virtanen (2020)](https://doi.org/10.1038/s41592-019-0686-2)) to expand the orientation from well-defined features and define orientation in void space (between well-defined features and over orientational boundaries). The dilation kernel size is chosen to be $2\lambda$, where $\lambda$ is the characteristic wavelength of the pattern and is also the approximate distance between well-defined features. 
* (3) **Blending**: Performed via a median filter from `scipy.ndimage.median_filter`` ([P. Virtanen (2020)](https://doi.org/10.1038/s41592-019-0686-2)) to allow for effective transition in orientations between neighbouring well-defined features and across orientational boundaries. The blending kernel size is chosen to be $4\lambda$ so that the orientation is averaged from two layers of surrounding neighbouring features.

It is also important to note that this pattern orientation method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is only applicable to images with **one** dominant pattern type. I.e., images with mixed patterns are invalid. 

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_3) should contain the following.

![](images/example_3_dir.png)

where **config** is the text-based configuration file, **example_3.py** is the Python script file, and **images/** holds the experimental square self-assembled nanostructure image ([C. Tang (2008)](https://doi.org/10.1126/science.1162950)) for analysis.

![](images/sqrAFM2.png)

### Configuration File Method - Setup

The configuration file provided in the example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_3) contains the following information:

	[general]
	image_name = sqrAFM2.png
	method = orientation

	[orientation]
	pattern_order = square

where **image_name** and **method** are required parameters that specify the image filename and method used for analysis.

The method outlined in the configuration file will also have its own header with specific parameters. The orientation method may contain up to one parameter. Note that default refers to the default value if the parameter is excluded from the configuration file.

**pattern_order** `str`

* The pattern order (symmetry) observed in the image. Options are `stripe`, `square`, `hexagonal`
* This parameter does not have a default value

### Configuration File Method - Run

Please ensure that `shapelets` is properly installed before proceeding. 

Navigate your terminal to "shapelets/examples/example_3". When you are ready, execute ``shapelets config`` in the command line.

Depending on your computer hardware, the iterative convergence scheme may take a couple of minutes.

The output (shown below) will then be available in "shapelets/examples/example_3/output" containing the mask (top left), dilated feature orientation (top right), smoothed orientation result, and the smoothed orientation result superimposed onto the original pattern (shown below, respectively).

![](images/sqrAFM2_orientation_maskedresp.png)
![](images/sqrAFM2_orientation_dilate.png)

![](images/sqrAFM2_orientation_blend.png)
![](images/sqrAFM2_orientation_overlay.png)

### Scripting Method 

For users comfortable with Python programming, the example_3.py file is structured to run the same analysis as described previously. The outputs will appear in the same directory.

## Example 4 - Galactic Image Decomposition

This example demonstrates the decomposition and reconstruction of images of galaxies ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)) using the ``shapelets.astronomy`` submodule.

This example can be run in two different ways:
* (1) text-based configuration files (shown here), and 
* (2) programmatically via script-based Python programming (`example_4.py`)

### Overview

The astronomical intensity/pixel data collected from the Hubble telecsope is is stored in a .fits file.
Flexible Image Transport System (or FITS) ([S. Allen (2005)](https://fits.gsfc.nasa.gov/rfc4047.txt)) were designed to standarize the exchange of astronomical image data between observatories.
FITS provides a method to transport arrays and tables of data alongside its related metadata. 

These intesities represent localized celestial objects (such as galaxies) that, once seperated from the original image, can be decomposed into a linear combination of shapelet functions. The method contains four (4) main steps:

* (1) **Source Extractor**: using Source Extractor ([E. Bertin (1996)](https://ui.adsabs.harvard.edu/link_gateway/1996A&AS..117..393B/doi:10.1051/aas:1996164)), subdomains containing localized intensities are selected from the intensity data, and categorized as galaxies or stars by pixel cluster size.

* (2) **Shapelet Projection**: the subdomain is projected onto a collection of 2D cartesian shapelets using a beta and centroid initially estimated by Source Extracter and $n$ such that $n_1 + n_2 \leq n_{max}$.

* (3) **Shapelet Parameter Optimization**: using formulae from ref. [A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), the object's centroid and characteristic size are estimated from the decomposed shapelet coefficients and used as an updated beta and centroid for a more optimized decomposition.

* (4) **Shapelet State Compression**: the shapelet coefficients are truncated, removing insignificant contributions to the shapelet representation. This truncated representation is then used to reconstruct the original image and the error associated with this reconstruction (i.e. from truncation) is computed.

Steps 2-3 are repeated for all galaxies identified by the **Source Extractor**.

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_4) should contain the following.

![](images/example_4_dir.png)

where **config** is the text-based configuration file, **example_4.py** is the Python script file, and **images/** holds the FITS file used in this example which contains a subset of images of galaxies from the Hubble Deep Field North ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)). This data is shown below as the linear (left) and mean normalized (right) greyscale images. 

![](images/galaxies_linear.png)
![](images/galaxies_std.png)

### Configuration File Method - Setup

The configuration file provided in the example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_4) contains the following information:

	[general] 
	method = galaxy_decompose
	fits_name = galaxies.fits 

	[galaxy_decompose] 
	shapelet_order = default 
	compression_order = 20 

where **image_name** and **method** are required parameters that specify the image filename and method used for analysis.

The method outlined in the configuration file will also have its own header with specific parameters. The **galaxy_decompose** method may contain up to two parameters. Note that default refers to the default value if the parameter is excluded from the configuration file.

**shapelet_order** `int`

* The maximum shapelet order (i.e. cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x))) to calculate coefficients such that $n_1 + n_2 \leq n_{max}$.
* default = 10

**compression_order** `int`

* The number of shapelet coefficients to use for final image reconstruction
* default = 25

**Note**

* You may only exclude parameters that have defaults

### Configuration File Method - Run

Please ensure that `shapelets` is properly installed before proceeding.

Navigate your terminal to "shapelets/examples/example_4". When you are ready, execute ``shapelets config`` in the command line.

The output (shown below) will be available in "shapelets/examples/example_4/output" containing the ellipses enclosing the locations of galaxies superimposed on the linear and mean normalized image (left). 

The second image contains information about the first decomposed galaxy, such as:
* the subdomain of the original image containing the galaxy,
* a reconstruction of the galaxy using the all calculated coefficients and a compressed set coefficients, and
* the compressed reconstruction's relative error

![](images/galaxies_map.png)
![](images/galaxies_decomposed.png)

### Scripting Method 

For users comfortable with Python programming, the example_4.py file is structured to run the same analysis as described previously. The outputs will appear in the same directory.

"""
