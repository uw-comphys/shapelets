# Example 1 - Response Distance Method

This example goes through the process of computing the response distance method ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) for self-assembly microscopy images using the ``shapelets.self_assembly`` submodule.

The files for this example can be found [here](https://github.com/uw-comphys/shapelets/tree/3c49c36c5e88330389c87328e7babc92702ae07e/examples/example_1).

**NOTE** - this example can be run in two different ways, and both methods are presented here.
* (1) the configuration-file based user interface [here](#config-method---config-setup)
* (2) importing neccessary ``shapelets`` submodules and methods in a script-based format [here](#scripting-method---example_1py-breakdown)


## Technical overview

The response distance ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) is calculated as:

$$ d_{i, j} = \min \| \vec{R} - \vec{r_{i,j}} \|_2 $$

where $\vec{r_{i,j}}$ denotes the given response vector at pixel location $\{i, j\}$ and $\vec{R}$ is the reference set (or subdomain) of response vectors.


## Directory overview

The example [directory](https://github.com/uw-comphys/shapelets/tree/3c49c36c5e88330389c87328e7babc92702ae07e/examples/example_1) should contain the following.

![](images/example_1_dir.png)

* **config** contains the configuration file to run example 1 via config method
* **example_1.py** contains the script to run example 1 via scripting method
* **images/** contains the simulated stripe self-assembly microscopy image ([R. Suderman (2015)](https://doi.org/10.1103/PhysRevE.91.033307)) used in this example, shown below

![](images/lamSIM1.png)


## Config method - config setup

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

## Method parameters

The parameters for the response distance method are outlined below.

Note these parameters are the same if using the configuration-file based method or the scripting method (example_1.py). 

These parameters are explained below, note that *default* refers to default behaviour if the parameter is excluded.

* **shapelet_order** 

	* int - integer, compute convolution for maximum shapelet order $m'$, i.e. $m \in [1, m']$
	* default = $m'$ computed by the higher-order shapelet algorithm ([M.P. Tino (2023)](REFTINO))

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


## Config method - running config

This config file is setup to compute the response distance for images/lamSIM1.png with a user-defined subdomain already provided in the config.

Navigate your terminal to "shapelets/examples/example_1". 

When you are ready, type ``shapelets config``.

The output (shown below) will be available in "shapelets/examples/example_1/output" containing the response distance scalar field (top) as well as this field superimposed onto the original pattern (bottom).

![](images/lamSIM1_response_distance_k20.png)

![](images/lamSIM1_response_distance_overlay_k20.png)


## Scripting method - example_1.py breakdown

This method is presented as an alternative to the configuration-file based user interface (config method).

**example_1.py** is pre-configured and requires **no additional modifications**.

The code breakdown is as follows,

* Section 1: importing modules - imports the necessary modules from the ``shapelets`` package
* Section 2: parameters - this contains the required parameters needed for the methods required to compute the response distance method (see [method parameters](#method-parameters) for details)
* Section 3: code - this contains the code to compute the response distance method which involves the following steps:

	* 3.1: image and output directory handling
	* 3.2: get the characteristic wavelength of the pattern
	* 3.3: get the convolutional response 
	* 3.4: compute the response distance 
	* 3.5: processing and saving the results to the **output/** directory 


## Scripting method - executing example_1.py

Navigate your terminal to "shapelets/examples/example_1". 

When you are ready, type ``python3 -m example_1`` (for MAC OS and LINUX users).

For WINDOWS users, please use ``python -m example_1`` .

The output will be available in "shapelets/examples/example_1/output".

To see the expected output, see the config method section [here](#config-method---running-config).

## Selecting subdomain bounds during runtime

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