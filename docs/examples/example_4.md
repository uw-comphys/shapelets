# Example 4 - Astronomical Image Decomposition

This example goes through the process of computing shapelet representations for a collection of galaxies using ``shapelets.astronomy`` submodule.

The files for this example can be found [here](https://github.com/mptino/shapelets/tree/742a88022330a6e18dc91b6a0dfe119c2d41da89/examples/example_4).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary ``shapelets`` submodules and methods in a script-based format [here](#scripting-method---example_4py-breakdown)


## Technical overview

The astronomical intensity/pixel data collected from the Hubble telecsope is is stored in a .fits file.
Flexible Image Transport System (or FITS) ([S. Allen (2005)](https://fits.gsfc.nasa.gov/rfc4047.txt)) were designed to standarize the exchange of astronomical image data between observatories.
FITS provides a method to transport arrays and tables of data alongside its related metadata. 

These intesities represent localized celestial objects (such as galaxies) that, once seperated from the original image, can be decomposed into a linear combination of shapelet functions. The method contains three (4) main steps:

* (1) **Source Extractor**: using Source Extractor ([E. Bertin (1996)](https://ui.adsabs.harvard.edu/link_gateway/1996A&AS..117..393B/doi:10.1051/aas:1996164)), subdomains containing localized intensities are selected from the intensity data, and catergorized as galaxies or stars by pixel cluster size.

* (2) **Shapelet Projection**: the subdomain is projected onto a collection of 2D cartesian shapelets using a beta and centroid initially estimated by Source Extracter and $n$ such that $n_1 + n_2 \leq n_{max}$.

* (3) **Shapelet Parameter Optimization**: using formulae from [A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), the object's centroid and characteristic size are estimated from the decomposed shapelet coefficients and used as an updated beta and centroid for more optimized decomposition.

* (4) **Shapelet State Compression**: the shapelet coefficients are truncated to a limited number of coefficients, removing insignificant contributions to the shapelet representation. This truncated representation is then used to reconstruct the original image and its respective error is calculated.

Steps 2-3 are repeated for all galaxies identified by Source Extractor


## Directory overview

The example [directory](https://github.com/mptino/shapelets/tree/742a88022330a6e18dc91b6a0dfe119c2d41da89/examples/example_4) should contain the following.

![](images/example_4_dir.png)

* **config** contains the configuration file to run example 4 via config method
* **example_4.py** contains the script to run example 4 via scripting method
* **images/** contains the fits used in this example, show below is the data with a linear colour scale scale and an image scaled from the mean and standard deviation (respectively)

![](images/galaxies_linear.png)

![](images/galaxies_std.png)


## Config method - config setup

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


## Method parameters

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


## Config method - running config

This config file is setup to perform galaxy decomposition for images/galaxies.fits.

Navigate your terminal to "shapelets/examples/example_4". 

When you are ready, type ``shapelets config``.

The output (first 2 images shown below) will be available in "shapelets/examples/example_4/output" . The first shows ellipses enclosing locations of galaxies superimposed on the linear and mean normalized image. The remaining images contain information about the first decomposed galaxy, including:
	* the subdomain of the original image containing the galaxy,
	* a reconstruction of the galaxy using the all calculated coefficients and a compressed set coefficients, and
	* the compressed reconstruction's relative error.

![](images/galaxies_map.png)

![](images/galaxies_decomposed.png)


## Scripting method - example_4.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_4.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the ``shapelets`` package
* Section 2: parameters - this contains the required parameters needed for the methods required to decompose an image containing multiple galaxies and reconstruct in terms of shapelet functions (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code for the decomposition which involves the following steps:

	* 3.1: loading .fits data and output directory handling
	* 3.2: identifying areas in the image that contain decomposable galaxies
	* 3.3: starting with the biggest galaxy, decomposes subdomain into a collection of shapelet coefficients


## Scripting method - executing example_4.py

Navigate your terminal to "shapelets/examples/example_4". 

When you are ready, type :code:`python3 -m example_4` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_4`` .

The output will be available in "shapelets/examples/example_4/output".

To see the expected output, see the config method section [here](#config-method---running-config).
