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

The example files and scripts can be found in the [github example directory](https://github.com/uw-comphys/shapelets/tree/main/examples).
Associated documentation can be found below and should be explored by all new users. 


## Example 1 - Response Distance

This example goes through the process of computing the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for self-assembly microscopy images using the ``shapelets.self_assembly`` submodule.

The files for this example can be found [here](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary shapelets submodules and methods in a script-based format [here](#scripting-method---example_1py-breakdown)

### Technical overview

The response distance ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) is calculated as:

$$ d_{i, j} = \min \| \vec{R} - \vec{r_{i,j}} \|_2 $$

where $\vec{r_{i,j}}$ denotes the given response vector at pixel location $\{i, j\}$ and $\vec{R}$ is the reference set (or subdomain) of response vectors.

### Directory overview

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1) should contain the following.

![](images/example_1_dir.png)

* **config** contains the configuration file to run example 1 via config method
* **example_1.py** contains the script to run example 1 via scripting method
* **images/** contains the simulated stripe self-assembly microscopy image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) used in this example, shown below

![](images/lamSIM1.png)

### Config method - config setup

The *general* section of the configuration file contains two parameters. 

	[general]
	image_name = lamSIM1.png
	method = response_distance

The "image_name" and "method" parameters are required.

Here the "method" parameter is chosen to be "response_distance" to indicate computation of the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)).

The *response_distance* section of the configuration file contains four parameters. 

	[response_distance]
	shapelet_order = default
	num_clusters = 20
	ux = [50, 80]
	uy = [150, 180]
		
These parameters are explained in detail in the [next section](#method-parameters).

### Method parameters

The parameters for the response distance method are outlined below.

Note these parameters are the same if using the configuration-file based method or the scripting method (example_1.py). 

These parameters are explained below, note that *default* refers to default behaviour if the parameter is excluded.

* **shapelet_order** 

	* int - integer, compute convolution for maximum shapelet order $m'$, i.e. $m \in [1, m']$
	* default = $m'$ computed by the higher-order shapelet algorithm ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4))

* **num_clusters**

	* int - integer (including 0, which will not perform k-means clustering and use all response vectors in subdomain)
	* default = 20 (see [T. Akdeniz (2018](https://doi.org/10.1088/1361-6528/aaf353]))

* **ux**

	* list - I.e., [10, 20], this would represent the lower and upper bound for the user-defined subdomain in x-direction respectively
	* default = 'default', user select x-bounds during runtime, see [here](#selecting-subdomain-bounds-during-runtime)

* **uy** 

	* list - I.e., [30, 40], this would represent the lower and upper bound for the user-defined subdomain in y-direction respectively
	* default = 'default', user select y-bounds during runtime, see [here](#selecting-subdomain-bounds-during-runtime)

**NOTE**

* You may only exclude parameters that have defaults (in this case, all 4 parameters have defaults)
* If you do not know the subdomain bounds (**ux** and **uy**), please see see [here](#selecting-subdomain-bounds-during-runtime).

### Config method - running config

This config file is setup to compute the response distance for images/lamSIM1.png with a user-defined subdomain already provided in the config.

Navigate your terminal to "shapelets/examples/example_1". 

When you are ready, type ``shapelets config``.

The output (shown below) will be available in "shapelets/examples/example_1/output" containing the response distance scalar field (top) as well as this field superimposed onto the original pattern (bottom).

![](images/lamSIM1_response_distance_k20.png)

![](images/lamSIM1_response_distance_overlay_k20.png)

### Scripting method - example_1.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_1.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the shapelets package
* Section 2: parameters - this contains the required parameters needed for the methods required to compute the response distance method (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code to compute the response distance method which involves the following steps:

	* 3.1: image and output directory handling
	* 3.2: get the characteristic wavelength of the pattern
	* 3.3: get the convolutional response 
	* 3.4: compute the response distance 
	* 3.5: processing and saving the results to the **output/** directory 

### Scripting method - executing example_1.py

Navigate your terminal to "shapelets/examples/example_1". 

When you are ready, type ``python3 -m example_1`` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_1`` .

The output will be available in "shapelets/examples/example_1/output".

To see the expected output, see the config method section [here](#config-method---running-config).

### Selecting subdomain bounds during runtime

If you are computing the response distance method for the first time on a new image, you will typically not know the reference subdomain bounds (i.e., parameters **ux** and **uy**) a priori. 

Adjustments required:

* config method - simply remove the **ux** and **uy** parameters
* scripting method - comment out the **ux** and **uy** statements in **example_1.py**

Follow the same steps for the config or scripting method, depending on your preference.

**Selecting bounds during runtime:**

After performing ``shapelets config`` (config method) or ``python3 -m example_1`` (scripting method), you will immediately be prompted to select four (4) points that represent the four corners/bounds of the reference subdomain

* use ``a`` to select a corner (bound) (in no particular order), 
* ``backspace/delete`` to remove the most recently selected corner, and 
* ``enter`` when you have finished selecting 4 points/corners 

**NOTE** 

* You may use the **magnifying glass** (bottom left) to zoom in on a specific region
* You may use the **left arrow** (bottom left) to return to original zoom
* Failure to choose 4 points/corners (i.e., choosing less or more than 4) will restart the process automatically
* It is critical to choose a region of the pattern that is appears to contain zero observable defects to maximize the response distance results

## Example 2 - Defect Identification

This example goes through the process of computing the defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) for self-assembly microscopy images using the ``shapelets.self_assembly`` submodule.

The files for this example can be found [here](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary shapelets submodules and methods in a script-based format [here](#scripting-method---example_2py-breakdown)

### Technical overview

The defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is a modification of the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)).

The user is required to manually select the clusters associated with defects or defect structures, and the *defect response distance* ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is computed for each cluster. 

The *defect response distance* ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) is similar to the response distance ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)), but the reference subdomain is the centroid response vector of each cluster (and not a set of reference response vectors). 

I.e., for a given cluster $C$ with centroid $C_c$, the defect response distance is computed as:

$$ d_i = \| C_c - c_i \|_2 $$

where $c_i$ is a cluster response vector belonging to cluster $C$ and is computed for all response vectors in each cluster.

The key observation is that cluster response vectors with larger defect response distances are more "defect-like", allowing use of the defect response distance as a quantitative measure of "defect intensity" ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)).

### Directory overview

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2) should contain the following.

![](images/example_2_dir.png)

* **config** contains the configuration file to run example 2 via config method
* **example_2.py** contains the script to run example 2 via scripting method
* **images/** contains the simulated hexagonal self-assembly microscopy image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) used in this example, shown below

![](images/hexSIM1.png)

### Config method - config setup

The *general* section of the configuration file contains two parameters. 

	[general]
	image_name = hexSIM1.png
	method = identify_defects

The "image_name" and "method" parameters are required.

Here the "method" parameter is chosen to be "identify_defects" to indicate computation of the defect identification method ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)).

The *identify_defects* section of the configuration file contains two parameters.

	[identify_defects]
	pattern_order = hexagonal
	num_clusters = 10
	
These parameters are explained in detail in the [next section](#method-parameters).

### Method parameters

The parameters for the defect identification method are outlined below.

Note these parameters are the same if using the configuration-file based method or the scripting method (example_2.py). 

These parameters are explained below, note that *default* refers to default behaviour if the parameter is excluded.

* **pattern_order**

	* stripe - used when image contains a stripe self-assembly pattern
	* square - used when image contains a square self-assembly pattern
	* hexagonal - used when image contains a hexagonal self-assembly pattern
	* default = not applicable

* **num_clusters** 

	* int - integer (0 not accepted)
	* default (if pattern_order = stripe) = 4
	* default (if pattern_order = square) = 8
	* default (if pattern_order = hexagonal) = 10

**NOTE**

* The "pattern_order" parameter does not have a default value; failure to provide a value will throw an error
* The "num_clusters" parameter minimum values are the same as the default values provided above
* If a value is given for "num_clusters" that is below the minimum (default) value, the code will defer to the minimum value instead of throwing an error

### Config method - running config

This config file is setup for the defect identification method for images/hexSIM1.png.

Navigate your terminal to "shapelets/examples/example_2". 

When you are ready, type ``shapelets config``.

You will then be prompted to select the clusters you wish to identify as associated with defects or defect structures, follow these instructions:

* use ``a`` to select a cluster (in no particular order, and duplicates are handled appropriately), 
* ``backspace/delete`` to remove the most recently selected cluster, and 
* ``enter`` when you have finished selecting clusters

**NOTE** 

* You may use the **magnifying glass** (bottom left) to zoom in on a specific region
* You may use the **left arrow** (bottom left) to return to original zoom

The outputs (shown below) will then be available in "shapelets/examples/example_2/output" containing the location of each cluster, radar chart of centroid response vectors, the defect response distance scalar field, and this field superimposed onto the original pattern.

For this example, the clusters 2, 5, and 8 were chosen when the user was prompted to select clusters associated with topological defects or defect structures. The first image shows the visual representation of each cluster, followed by the radar chart plots of the cluster centroids and their respective shapelet weights. The last two images contain the defect response distance scalar field, along with this scalar field superimposed onto the original image.

![](images/hexSIM1_defectid_clustloc_k10.png)

![](images/hexSIM1_defectid_rc_k10.png)

![](images/hexSIM1_defectid_drd_k10.png)

![](images/hexSIM1_defectid_drd_overlay_k10.png)

### Scripting method - example_2.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_2.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the shapelets package
* Section 2: parameters - this contains the required parameters needed for the methods required to compute the defect identification method (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code to compute the defect identification method which involves the following steps:

	* 3.1: image and output directory handling
	* 3.2: get the characteristic wavelength of the pattern
	* 3.3: get the convolutional response 
	* 3.4: compute the defect identification method
	* 3.5: processing and saving the results to the **output/** directory 

### Scripting method - executing example_2.py

Navigate your terminal to "shapelets/examples/example_2". 

When you are ready, type :code:`python3 -m example_2` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_2`` .

You will then be prompted to select the clusters you wish to identify as associated with defects or defect structures, follow these instructions:

* use ``a`` to select a cluster (in no particular order, and duplicates are handled appropriately), 
* ``backspace/delete`` to remove the most recently selected cluster, and 
* ``enter`` when you have finished selecting clusters

**NOTE** 

* You may use the **magnifying glass** (bottom left) to zoom in on a specific region
* You may use the **left arrow** (bottom left) to return to original zoom

The output will be available in "shapelets/examples/example_2/output".

To see the expected output, see the config method section [here](#config-method---running-config).

## Example 3 - Local Pattern Orientation

This example goes through the process of computing the local pattern orientation ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) for self-assembly microscopy images using the ``shapelets.self_assembly`` submodule.

The files for this example can be found [here](https://github.com/uw-comphys/shapelets/tree/main/examples/example_3).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary shapelets submodules and methods in a script-based format [here](#scripting-method---example_3py-breakdown)

### Technical overview

Local pattern orientation is concerned with the relative orientation of nanostructure along grain boundaries and in between grains.

The method to compute the local pattern orientation ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) contains three (3) main steps:

* (1) **Masking**: Masking is performed for well-defined features using a specific response threshold. This threshold is found via an interative scheme. Only the orientation values from these well-defined features included in the mask are used.
* (2) **Dilation**: Dilation (via morphological greyscale dilation) is used to expand the orientation from well-defined features and ultimately define orientation in void space (between well-defined features and over orientational boundaries). The dilation kernel size is chosen to be $2\lambda$, where $\lambda$ is the characteristic wavelength of the pattern and is also the approximate distance between well-defined features. 
* (3) **Blending**: Blending (or smoothing) is performed via a median filter to allow for effective transition in orientations between neighbouring well-defined features and across orientational boundaries. The blending kernel size is chosen to be $4\lambda$ so that the orientation is averaged from two layers of surrounding neighbouring features.

**NOTE** - dilation and blending are achieved through the ``scipy.ndimage.grey_dilation`` and ``scipy.ndimage.median_filter`` methods respectively. They are available from ``scipy.ndimage`` ([P. Virtanen (2020)](https://doi.org/10.1038/s41592-019-0686-2)).

### Directory overview

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_3) should contain the following.

![](images/example_3_dir.png)

* **config** contains the configuration file to run example 3 via config method
* **example_3.py** contains the script to run example 3 via scripting method
* **images/** contains the square self-assembly AFM image ([C. Tang (2008)](https://doi.org/10.1126/science.1162950)) used in this example, shown below

![](images/sqrAFM2.png)

### Config method - config setup

The *general* section of the configuration file contains two parameters. 

	[general]
	image_name = sqrAFM2.png
	method = orientation

The "image_name" and "method" parameters are required.

Here the "method" parameter is chosen to be "orientation" to indicate computation of local pattern orientation ([M.P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)).

The *orientation* section of the configuration file contains one parameter.

	[orientation]
	pattern_order = square

These parameters are explained in detail in the [next section](#method-parameters).

### Method parameters

The parameters for the local pattern orientation method are outlined below.

Note these parameters are the same if using the configuration-file based method or the scripting method (example_3.py). 

These parameters are explained below, note that *default* refers to default behaviour if the parameter is excluded.

* **pattern_order**

	* stripe - used when image contains a stripe self-assembly pattern
	* square - used when image contains a square self-assembly pattern
	* hexagonal - used when image contains a hexagonal self-assembly pattern
	* default = not applicable

**Note**

* The "pattern_order" parameter does not have a default value; failure to provide a value will throw an error
* The image you intend to analyze **should not** contain a mix of pattern orders; i.e., it should only contain one pattern order throughout the entire image

### Config method - running config

This config file is setup to compute the local pattern orientation for images/sqrAFM2.png.

Navigate your terminal to "shapelets/examples/example_3". 

When you are ready, type ``shapelets config``.

Depending on your computer resources, the convergence scheme may take a couple of minutes.

The outputs (shown below) will then be available in "shapelets/examples/example_3/output" containing the mask, dilated feature orientation, smoothed orientation result, and the smoothed orientation result superimposed onto the original pattern (shown below, respectively).

![](images/sqrAFM2_orientation_maskedresp.png)

![](images/sqrAFM2_orientation_dilate.png)

![](images/sqrAFM2_orientation_blend.png)

![](images/sqrAFM2_orientation_overlay.png)

### Scripting method - example_3.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_3.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the shapelets package
* Section 2: parameters - this contains the required parameters needed for the methods required to compute the local pattern orientation method (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code to compute the local pattern orientation which involves the following steps:

	* 3.1: image and output directory handling
	* 3.2: get the characteristic wavelength of the pattern
	* 3.3: get the convolutional response 
	* 3.4: compute the local pattern orientation
	* 3.5: processing and saving the results to the **output/** directory 

### Scripting method - executing example_3.py

Navigate your terminal to "shapelets/examples/example_3". 

When you are ready, type :code:`python3 -m example_3` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_3`` .

The output will be available in "shapelets/examples/example_3/output".

To see the expected output, see the config method section [here](#config-method---running-config).

## Example 4 - Galactic Image Decomposition

This example goes through the process of computing shapelet representations for a collection of galaxies using ``shapelets.astronomy`` submodule.

The files for this example can be found [here](https://github.com/uw-comphys/shapelets/tree/main/examples/example_4).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary shapelets submodules and methods in a script-based format [here](#scripting-method---example_4py-breakdown)

### Technical overview

The astronomical intensity/pixel data collected from the Hubble telecsope is is stored in a .fits file.
Flexible Image Transport System (or FITS) ([S. Allen (2005)](https://fits.gsfc.nasa.gov/rfc4047.txt)) were designed to standarize the exchange of astronomical image data between observatories.
FITS provides a method to transport arrays and tables of data alongside its related metadata. 

These intesities represent localized celestial objects (such as galaxies) that, once seperated from the original image, can be decomposed into a linear combination of shapelet functions. The method contains three (4) main steps:

* (1) **Source Extractor**: using Source Extractor ([E. Bertin (1996)](https://ui.adsabs.harvard.edu/link_gateway/1996A&AS..117..393B/doi:10.1051/aas:1996164)), subdomains containing localized intensities are selected from the intensity data, and catergorized as galaxies or stars by pixel cluster size.

* (2) **Shapelet Projection**: the subdomain is projected onto a collection of 2D cartesian shapelets using a beta and centroid initially estimated by Source Extracter and $n$ such that $n_1 + n_2 \leq n_{max}$.

* (3) **Shapelet Parameter Optimization**: using formulae from [A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), the object's centroid and characteristic size are estimated from the decomposed shapelet coefficients and used as an updated beta and centroid for more optimized decomposition.

* (4) **Shapelet State Compression**: the shapelet coefficients are truncated to a limited number of coefficients, removing insignificant contributions to the shapelet representation. This truncated representation is then used to reconstruct the original image and its respective error is calculated.

Steps 2-3 are repeated for all galaxies identified by Source Extractor

### Directory overview

The example [directory](https://github.com/uw-comphys/shapelets/tree/main/examples/example_4) should contain the following.

![](images/example_4_dir.png)

* **config** contains the configuration file to run example 4 via config method
* **example_4.py** contains the script to run example 4 via scripting method
* **images/** contains the fits used in this example, show below is the data with a linear colour scale scale and an image scaled from the mean and standard deviation (respectively)

![](images/galaxies_linear.png)

![](images/galaxies_std.png)

### Config method - config setup

The *general* section of the configuration file contains two parameters. 

	[general] 
	method = galaxy_decompose
	fits_name = galaxies.fits 

The "method" and "fits_name" parameter is required.

The *galaxy_decompose* section of the configuration file contains two parameters. 

	[galaxy_decompose] 
	shapelet_order = default 
	compression_order = 20 

These parameters are explained in detail in the [next section](#method-parameters).

### Method parameters

The parameters for the galaxy decomposition are outlined below.

Note these parameters are the same if using the configuration-file based method or the scripting method (example_4.py). 

These parameters are explained below, note that *default* refers to default behaviour if the parameter is excluded.

* **fits_name** 

	* str - string, path to the .fits data file containing the astronomical data

* **shapelet_order** 

	* int - integer, maximum shapelet order to calculate coefficients such that $n_1 + n_2 \leq n_{max}$
	* default = 10

* **compression_order** 

	* int - integer,  number of shapelet coefficients to use for final image reconstruction
	* default = 25

**Note**

* You may only exclude parameters that have defaults

### Config method - running config

This config file is setup to perform galaxy decomposition for images/galaxies.fits.

Navigate your terminal to "shapelets/examples/example_4". 

When you are ready, type ``shapelets config``.

The output (first 2 images shown below) will be available in "shapelets/examples/example_4/output" . The first shows ellipses enclosing locations of galaxies superimposed on the linear and mean normalized image. The remaining images contain information about the first decomposed galaxy, including:
	* the subdomain of the original image containing the galaxy,
	* a reconstruction of the galaxy using the all calculated coefficients and a compressed set coefficients, and
	* the compressed reconstruction's relative error.

![](images/galaxies_map.png)

![](images/galaxies_decomposed.png)

### Scripting method - example_4.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_4.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the shapelets package
* Section 2: parameters - this contains the required parameters needed for the methods required to decompose an image containing multiple galaxies and reconstruct in terms of shapelet functions (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code for the decomposition which involves the following steps:

	* 3.1: loading .fits data and output directory handling
	* 3.2: identifying areas in the image that contain decomposable galaxies
	* 3.3: starting with the biggest galaxy, decomposes subdomain into a collection of shapelet coefficients

### Scripting method - executing example_4.py

Navigate your terminal to "shapelets/examples/example_4". 

When you are ready, type :code:`python3 -m example_4` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_4`` .

The output will be available in "shapelets/examples/example_4/output".

To see the expected output, see the config method section [here](#config-method---running-config).

"""