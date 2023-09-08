---
title: 'Shapelets: A Python package implementing shapelet functions and their applications'
tags:
 - Python
 - shapelets
 - self-assembly
 - astronomy
 - image processing
 - machine learning
authors:
 - name: Matthew Peres Tino
   orcid: 0009-0005-6832-1761
   affiliation: 1
 - name: Abbas Yusuf Abdulaziz
   orcid: XXXX-XXXX-XXXX-XXXX
   affiliation: 1
 - name: Nasser Mohieddin Abukhdeir^[Corresponding author]
   orcid: 0000-0002-1772-0376
   affiliation: "1, 2, 3" # Need quotes for multiple affiliations
 - name: Robert Suderman
   orcid: XXXX-XXXX-XXXX-XXXX
   affiliation: 4
 - name: Thomas Akdeniz
   orcid: XXXX-XXXX-XXXX-XXXX
   affiliation: 5
affiliations:
 - name: Department of Chemical Engineering, University of Waterloo, Ontario, Canada
   index: 1
 - name: Department of Physics and Astronomy, University of Waterloo, Ontario, Canada
   index: 2
 - name: Waterloo Institute for Nanotechnology, University of Waterloo, Ontario, Canada
   index: 3
 - name: Google Inc.
   index: 4
 - name: East Coast Asset Management SEZC
   index: 5
date:
bibliography: paper.bib
---

# Summary

`Shapelets` is a Python-based software package that implements several shapelet functions [@Refregier2003] and some of their significant applications in science and astronomy. Shapelet functions are a complete and orthogonal set of localized basis functions with mathematical properties convenient for manipulation and analysis of images from a broad range of applications. Over the past few decades, there have been several different shapelet function formulations developed and applied in the areas of astronomy/astrophysics [@Refregier2003; @Massey2005; @Lentati2015; @Birrer2015; @Desvignes2016; @Berge2019], self-assembly nanomaterials [@Suderman2015; @Akdeniz2018; @Tino2023], computational neuroscience [@Victor2006; @Sharpee2009], and medical imaging [@Weissman2004].

The `shapelets` software package provides reference implementations and documentation for four different shapelet formulations: cartesian [@Refregier2003], polar [@Massey2005], orthonormal polar with constant radial scale [@Akdeniz2018], and exponential [@Berge2019]. Additionally, the `shapelets` package provides reference implementations of several applications of shapelet functions in astronomy (galactic image decomposition and reconstruction [@Refregier2003; @Massey2005]) and self-assembly (quantification of nanostructure order [@Suderman2015; @Akdeniz2018; @Tino2023]). The coding style of `shapelets` is based on that of [`scipy.special`](https://docs.scipy.org/doc/scipy/reference/special.html) [@scipy].

For ease of use, `shapelets` also provides a text configuration-based user interface and Python [entry points](https://packaging.python.org/en/latest/specifications/entry-points/) (custom terminal commands) to improve accessibility for a broad range of potential users in science and engineering, including those without a strong Python programming background. For example, the configuration-file based interface can be invoked via `shapelets config`, and running the unit tests associated with the package can be invoked via `shapelets-test`.

Lastly, the `shapelets` package includes a set of detailed examples which demonstrate usage of the software through both the text configuration-based and programmatic interfaces. These examples include both astronomy and self-assembly applications, providing users with a basis for developing their own applications of the package and shapelets functions, in general.


# Statement of Need

Shapelets are a class of complete localized orthogonal basis functions with a broad range of applications in image processing and reconstruction [@Refregier2003; @Massey2005; @Suderman2015; @Akdeniz2018; @Tino2023]. Despite their increasingly widespread use, there currently is no single software package that is both broadly accessible (e.g. written in Python or other high-level programming language) and implements several useful applications. Currently, there exists an open-source astronomy-focused [shapelet software package](https://www.astro.dur.ac.uk/~rjm/shapelets/code/index.php) [@Massey2005], however, it is written in the [Interactive Data Language (IDL) programming language](https://en.wikipedia.org/wiki/IDL_(programming_language)) which is not widely used in the science and engineering communities. Furthermore, this package has not been updated in over a decade. Given the increasingly broad usage of shapelets in areas outside of astronomy/astrophysics, an open-source Python-based shapelets software package would provide access to these functions and their applications to a larger community, along with facilitating open-source scientific software development through the existence of a centralized software package that allows for contribution and collaboration.

Similarly, quantification of structure/property relationships for nanomaterials is critical for continued progress in research [@Abukhdeir2016]. This is especially true for nanomaterials with complex spatially-varying patterns, such as self-assembly materials [@Abukhdeir2016]. There are other methods to quantify nanostructure order, such as bond-orientational order analysis [@Brock1992], but these do not provide pixel-scale information and do not have readily available open-source software implementations. Methods to quantify nanostructure order, such as those implemented in the `shapelets` package, would significantly advance (nano)materials research and provide researchers with accessible tools to quantify order for their own material images.

The overall aim of the `shapelets` package is to address these needs through (1) providing well-documented and accessible code for researchers interested in using these shapelet functions and existing applications and (2) promoting open-source collaboration for future development of shapelet-related research.

# Features

The table below summarizes the different shapelet functions implemented in the `shapelets` package.

| Shapelet Functions     | Description                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cartesian     | Cartesian shapelets from ref. [@Refregier2003] via `shapelets.functions.cartesian1D`, `shapelets.functions.cartesian2D`            |
| Polar             | Polar shapelets from ref. [@Massey2005] via `shapelets.functions.polar2D`                                                                       |
| Orthonormal polar  | Orthonormal polar shapelets with constant radial scale from ref. [@Akdeniz2018] via  `shapelets.functions.orthonormalpolar2D`                  |
| Exponential   | Exponential shapelets from ref. [@Berge2019] via `shapelets.functions.exponential1D`, `shapelets.functions.exponential2D`          |

The table below summarizes the specific shapelet applications implemented in this package.

| Shapelet Applications    		  | Description                                                                                                                       |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Galaxy decomposition            | Galactic image decomposition & reconstruction [@Refregier2003] via `shapelets.astronomy.TODO`                                                |
| Response distance         | Response distance method for self-assembly microscopy imaging from refs. [@Suderman2015; @Akdeniz2018] via `shapelets.self_assembly.rdistance` |
| Orientation                     | Local pattern orientation for self-assembly microscopy imaging from ref. [@Tino2023] via `shapelets.self_assembly.orientation`                    |
| Defect identification     | Defect identification method for self-assembly microscopy imaging from ref. [@Tino2023] via `shapelets.self_assembly.defectid`                    |

More information, such as installation instructions and application-specific examples can be found in the package [README](https://github.com/uw-comphys/shapelets) file.

# User Interface Methods

The `shapelets` python package can be used in two different ways: text-based configuration files and directly via interactive or script-based Python programming.

## Understanding the Configuration File Method

The text-based user interface for `shapelets` is centered around configuration files and the CLI (command line interface). Each use of the shapelets package (via configuration files) should have a main directory (here called "shapelets_example") with standard sub-directories and required files as shown below.

![](images/user_interface.png){ width=150%, height=150%}

The main (shapelets_example) directory contains the main configuration file (e.g., `config`) which is a plain-text file specifying specific parameters or methods to be used. Acceptable parameters and options for the configuration file can be found throughout the [examples](https://github.com/uw-comphys/shapelets/tree/main/examples), depending on the shapelet-based method being applied.

The `images/` subdirectory contains the data for image analysis and must be present. The `output/` subdirectory is created by the `shapelets` software and contains output data/images based on the analysis directed in the `config`.

Alternatively, the Python-based software interface of the `shapelets` package can be used either interactively or via scripting through standard import of either shapelet function implementations and/or application submodules.


# Examples of Usage

For each example included in the package, implementations using both the configuration file and programming-based interfaces are demonstrated. Several detailed image processing examples were developed that demonstrate the use and capabilities of the shapelets package for both astronomy and self-assembly related applications. See [here](https://github.com/uw-comphys/shapelets/tree/main/examples) and [here](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) for examples and their associated documentation, respectively.

Examples 1-3 demonstrate use of the `shapelets.self_assembly` module, with specific applications for the response distance method [@Suderman2015], local pattern orientation [@Tino2023], and defect identification method [@Tino2023].
Example 4 demonstrates use of the `shapelets.astronomy` submodule for the decomposition and reconstruction of galactic images. All examples have instructions to use the `shapelets` package via configuration files or importing relevant submodules in pre-configured `.py` files (scripting).

## Example 1 - Response Distance Method

[Example 1](https://github.com/uw-comphys/shapelets/tree/main/examples/example_1) demonstrates use of the `shapelets.self_assembly` submodule to compute the response distance method [@Suderman2015]. This example will use a simulated stripe self-assembly microscopy image from ref. [@Suderman2015], shown below.

![](images/lamSIM1.png){ width=20%, height=20%}

### Response Distance

The response distance [@Suderman2015] is computed as $$d_{i, j} = \min \| \vec{R} - \vec{r_{i,j}} \|_2$$ where $\vec{r_{i,j}}$ denotes the given response vector at pixel location ${i, j}$ and $\vec{R}$ is the reference set of response vectors. See ref. [@Suderman2015] for more details.

### Configuration file Method

The configuration file (`config`) contains the following information,

	[general]
	image_name = lamSIM1.png
	method = response_distance

	[response_distance]
	shapelet_order = default
	num_clusters = 20
	ux = [50, 80]
	uy = [150, 180]

where

* *shapelet_order* details the maximum shapelet order ($m'$) to use during convolution (i.e., $m = [1, m']$; see ref. [@Tino2023]] for more details),
* *num_clusters* details the number of clusters required for k-means clustering [@Wu2012], and
* [*ux*, *uy*] detail the coordinates of the user-defined reference subdomain required for the response distance method [@Suderman2015].

Possible values for each parameter, including default values where applicable, are available in the [documentation](https://github.com/uw-comphys/shapelets/blob/main/docs/examples/example_1.rst) under the section "Method parameters".

To run this example, navigate the terminal directory to "shapelets/examples/example_1". Then, type `shapelets config` into your command line. The outputs will be available in "shapelets/examples/example_1/output", containing the following two images corresponding to the response distance scalar field and the superimposed field on the original image.

![](images/lamSIM1_response_distance_k20.png){ width=20%, height=20%}
![](images/lamSIM1_response_distance_overlay_k20.png){ width=20%, height=20%}

**Note** - typically, you may not know the **ux** and **uy** parameters for your image when computing the response distance for the first time. If this is the case, please see the section "Selecting subdomain bounds during runtime" in the [Example 1 documentation](https://github.com/uw-comphys/shapelets/blob/main/docs/examples/example_1.rst).

### Scripting Method

For users wishing to interact with the `shapelets` package in a more traditional format, the `example_1.py` file is setup to obtain the same outputs as seen above without any code modifications needed.

After executing `example_1.py`, the outputs (shown above) will be available in "shapelets/examples/example_1/output".

## Example 2 - Defect Identification Method


[Example 2](https://github.com/uw-comphys/shapelets/tree/main/examples/example_2) demonstrates use of the `shapelets.self_assembly` submodule to compute the defect identification method [@Tino2023]. This example will use a simulated hexagonal self-assembly microscopy image from ref. [@Suderman2015], shown below.

![](images/hexSIM1.png){ width=20%, height=20%}

### Defect Identification Method

The defect identification method [@Tino2023] is a modification from the response distance method from ref. [@Suderman2015].

The user is required to manually select the clusters associated with defects or defect structures, and the *defect response distance* is computed for each cluster.

The *defect response distance* is similar to the response distance, but the reference subdomain is the centroid response vector of each cluster (and not a set of reference response vectors).

I.e., for a given cluster $C$ with centroid $C_c$, the defect response distance is computed as $$d_i = \| C_c - c_i \|_2$$ where $c_i$ is a cluster response vector belonging to cluster $C$ and is computed for all response vectors in *each* cluster.

### Configuration file Method

The configuration file (`config`) contains the following information,

	[general]
	image_name = hexSIM1.png
	method = identify_defects

	[identify_defects]
	pattern_order = hexagonal
	num_clusters = 10

where

* *pattern_order* details the dominant pattern symmetry in the image *image_name*, and
* *num_clusters* details the number of clusters desired for k-means clustering [@Wu2012].

Possible values for each parameter, including default values where applicable, are available in the [documentation](https://github.com/uw-comphys/shapelets/blob/main/docs/examples/example_2.rst) under section "Method parameters".

To run this example, navigate the terminal directory to "shapelets/examples/example_2". Then, type `shapelets config` into your command line.

You will be required to select the clusters associated with defects or defect structures during runtime. Details for this specific process can be found in the [documentation](https://github.com/uw-comphys/shapelets/blob/main/docs/examples/example_2.rst) under section "Config method - running config" or "Scripting method - executing example_2.py", depending on the preferred package interface method.

The outputs will be available in "shapelets/examples/example_2/output", containing the following four images corresponding to (1) the locations of each cluster through the image, (2) radar chart representations of the centroid response vectors from k-means clustering [@Wu2012], (3) the defect response distance scalar field, and (4) this scalar field superimposed onto the original image.

![](images/hexSIM1_defectid_clustloc_k10.png){ width=20%, height=20%}
![](images/hexSIM1_defectid_rc_k10.png){ width=20%, height=20%}

![](images/hexSIM1_defectid_drd_k10.png){ width=20%, height=20%}
![](images/hexSIM1_defectid_drd_overlay_k10.png){ width=20%, height=20%}

### Scripting Method

For users wishing to interact with the `shapelets` package in a more traditional format, the `example_2.py` file is setup to obtain the same outputs as seen above without any code modifications needed.

After executing `example_2.py`, the outputs (shown above) will be available in "shapelets/examples/example_2/output".

## Example 4 - Galactic Image Decomposition & Reconstruction

TODO (Abbas)

# Acknowledgements

This research was supported by the Natural Sciences and Engineering Research Council of Canada (NSERC) and the Digital Research Alliance of Canada.

# References
