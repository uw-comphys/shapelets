# Example 3 - Local Pattern Orientation

This example goes through the process of computing the local pattern orientation ([M.P. Tino (2023)](REFTINO)) for self-assembly microscopy images using the ``shapelets.self_assembly`` submodule.

The files for this example can be found [here](https://github.com/mptino/shapelets/tree/742a88022330a6e18dc91b6a0dfe119c2d41da89/examples/example_3).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary ``shapelets`` submodules and methods in a script-based format [here](#scripting-method---example_3py-breakdown)


## Technical overview

Local pattern orientation is concerned with the relative orientation of nanostructure along grain boundaries and in between grains.

The method to compute the local pattern orientation ([M.P. Tino (2023)](REFTINO)) contains three (3) main steps:

* (1) **Masking**: Masking is performed for well-defined features using a specific response threshold. This threshold is found via an interative scheme. Only the orientation values from these well-defined features included in the mask are used.
* (2) **Dilation**: Dilation (via morphological greyscale dilation) is used to expand the orientation from well-defined features and ultimately define orientation in void space (between well-defined features and over orientational boundaries). The dilation kernel size is chosen to be $2\lambda$, where $\lambda$ is the characteristic wavelength of the pattern and is also the approximate distance between well-defined features. 
* (3) **Blending**: Blending (or smoothing) is performed via a median filter to allow for effective transition in orientations between neighbouring well-defined features and across orientational boundaries. The blending kernel size is chosen to be $4\lambda$ so that the orientation is averaged from two layers of surrounding neighbouring features.

**NOTE** - dilation and blending are achieved through the ``scipy.ndimage.grey_dilation`` and ``scipy.ndimage.median_filter`` methods respectively. They are available from ``scipy.ndimage`` ([P. Virtanen (2020)](https://doi.org/10.1038/s41592-019-0686-2)).


## Directory overview

The example [directory](https://github.com/mptino/shapelets/tree/742a88022330a6e18dc91b6a0dfe119c2d41da89/examples/example_3) should contain the following.

![](images/example_3_dir.png)

* **config** contains the configuration file to run example 3 via config method
* **example_3.py** contains the script to run example 3 via scripting method
* **images/** contains the square self-assembly AFM image ([C. Tang (2008)](https://doi.org/10.1126/science.1162950)) used in this example, shown below

![](images/sqrAFM2.png)


## Config method - config setup

The *general* section of the configuration file contains two parameters. 

	[general]
	image_name = sqrAFM2.png
	method = orientation

The "image_name" and "method" parameters are required.

Here the "method" parameter is chosen to be "orientation" to indicate computation of local pattern orientation ([M.P. Tino (2023)](REFTINO)).

The *orientation* section of the configuration file contains one parameter.

	[orientation]
	pattern_order = square

These parameters are explained in detail in the [next section](#method-parameters).


## Method parameters

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


## Config method - running config

This config file is setup to compute the local pattern orientation for images/sqrAFM2.png.

Navigate your terminal to "shapelets/examples/example_3". 

When you are ready, type ``shapelets config``.

Depending on your computer resources, the convergence scheme may take a couple of minutes.

The outputs (shown below) will then be available in "shapelets/examples/example_3/output" containing the mask, dilated feature orientation, smoothed orientation result, and the smoothed orientation result superimposed onto the original pattern (shown below, respectively).

![](images/sqrAFM2_orientation_maskedresp.png)

![](images/sqrAFM2_orientation_dilate.png)

![](images/sqrAFM2_orientation_blend.png)

![](images/sqrAFM2_orientation_overlay.png)


## Scripting method - example_3.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_3.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the ``shapelets`` package
* Section 2: parameters - this contains the required parameters needed for the methods required to compute the local pattern orientation method (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code to compute the local pattern orientation which involves the following steps:

	* 3.1: image and output directory handling
	* 3.2: get the characteristic wavelength of the pattern
	* 3.3: get the convolutional response 
	* 3.4: compute the local pattern orientation
	* 3.5: processing and saving the results to the **output/** directory 


## Scripting method - executing example_3.py

Navigate your terminal to "shapelets/examples/example_3". 

When you are ready, type :code:`python3 -m example_3` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_3`` .

The output will be available in "shapelets/examples/example_3/output".

To see the expected output, see the config method section [here](#config-method---running-config).
