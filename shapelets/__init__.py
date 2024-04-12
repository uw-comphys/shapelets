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

# shapelets

[![DOI](https://joss.theoj.org/papers/10.21105/joss.06058/status.svg)](https://doi.org/10.21105/joss.06058)

## What is shapelets? 

Shapelets is a Python package that implements several shapelet functions and some of their significant applications in science and astronomy. Shapelet functions are a complete and orthogonal set of localized basis functions with mathematical properties convenient for manipulation and analysis of images from a broad range of applications.

Due to these properties, they have seen extensive use in recent years, including:

* Astronomy/astrophysics ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))
* Self-assembled nanomaterials ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4))
* Computational neuroscience ([J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5))
* Medical imaging ([J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760))

The shapelets package provides reference code and documentation for 4 shapelet function definitions: 

* Cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)), 
* Polar shapelets ([R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)),
* Orthonormal polar shapelets with constant radial scale ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353)), and 
* Exponential shapelets ([J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))

## Getting Started

New users should kindly follow these instructions to use the shapelets package:

1. If you have Python 3.10+ installed, you can install the shapelets package via pip from your terminal/command line: `pip install shapelets` 
2. If you do not have Python 3.10+ installed, consult the [installation guide](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html) for helpful instructions on Linux, Mac OS, and Windows machines.
3. Consult the [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html) to see specific applications implemented in the package and a walkthrough of how to interact with the package correctly.
4. Checkout other documentation, such as
    * [Custom Commands](https://uw-comphys.github.io/shapelets/shapelets/docs/custom_commands.html) - describes command-line arguments specifically designed for this package
    * [Package Interface](https://uw-comphys.github.io/shapelets/shapelets/docs/package_interface.html) - describes two different ways of using the `shapelets` package (configuration files or traditional Python programming)

If you plan to use the shapelets package for your own work, please cite appropriately using the [citation](#citation) below.

## Issues

If you encounter any **bugs** or **problems** with shapelets, please create a post using our package [issue tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images or code-snippets where appropriate. We will do our best to address these problems as fast and efficiently as possible.

## Contribute

The authors of the shapelets package welcome external contributions to the source code. This process will be easiest if users adhere to the contribution policy:

* Open an issue on the package [issue tracker](https://github.com/uw-comphys/shapelets/issues) clearly describing your intentions on code modifications or additions
* Ensure your modifications or additions adhere to the existing standard of the shapelets package, specifically detailed documentation for new methods (see existing methods for example documentation)
* Test your modifications to ensure that the core functionality of the package has not been altered by running the unit tests via the custom command: `shapelets-test`
* Once the issue has been discussed with a package author, you may open a pull request containing your modifications

## Citation

If you plan to use shapelets in your own work, please cite using the following Bibtex citation:

```
@article{TinoShapelets2024,
author = {Tino, Matthew Peres and Abdulaziz, Abbas Yusuf and Suderman, Robert and Akdeniz, Thomas and Abukhdeir, Nasser Mohieddin},
title = {Shapelets: A Python package implementing shapelet functions and their applications},
doi = {10.21105/joss.06058},
journal = {Journal of Open Source Software},
number = {95},
pages = {6058},
volume = {9},
year = {2024},
url = {https://joss.theoj.org/papers/10.21105/joss.06058}
}
```

## Authors

* Matthew Peres Tino
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz

"""
