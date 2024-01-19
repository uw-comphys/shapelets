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

# What is shapelets? 

shapelets is a python package that implements several shapelet functions and some of their significant applications in science and astronomy. These functions form a complete and orthonormal set, allowing them to capture complex geometries and information from any physical shape. Furthermore, shapelets are localized and can be scaled to match that of any physical feature. 

Due to these properties, they have seen extensive use in recent years, with several different formulations and applications:

* Astronomy/astrophysics ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))
* Nanomaterials ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4))
* Computational neuroscience ([J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5))
* Medical imaging ([J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760))

The shapelets package provides reference documentation and code for four (4) shapelet functions: 

* Cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)), 
* Polar shapelets ([R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)),
* Orthonormal polar shapelets with constant radial scale ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353)), and 
* Exponential shapelets ([J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))

# Getting Started

New users should kindly follow these instructions to use the shapelets package here:

1. Consult the [installation instructions](https://mptino.github.io/shapelets/shapelets/docs/installation.html) page to install the shapelets package.
2. Checkout the [custom commands and methods of usage](https://mptino.github.io/shapelets/shapelets/docs/usage.html) to see some important command-line features and how to interact with the shapelets package properly.
3. Checkout the [examples](https://mptino.github.io/shapelets/shapelets/docs/examples.html) page for descriptive examples of specific applications implemented for the shapelets package.

If you wish to contribute to the shapelets package, see the [contribution guidelines](#contribute).  

If you find an issue or bug while using the shapelets package? See the [issues](#issues) section for further details.

# Contribute

The authors of the shapelets package welcome external contributions to the source code. This process will be easiest if users adhere to the contribution policy:

* Open an issue on the package [issue tracker](https://github.com/uw-comphys/shapelets/issues) clearly describing your intentions on code modifications or additions
* Ensure your modifications or additions adhere to the existing standard of the shapelets package, specifically detailed documentation for new methods (see existing methods for example documentation)
* Test your modifications to ensure that the core functionality of the package has not been altered by running the unit tests via the custom command: `shapelets-test`
* Once the issue has been discussed with a package author, you may open a pull request containing your modifications

# Issues

If you encounter any **bugs** or **problems** with shapelets, please create a post using our package [issue tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images or code-snippets where appropriate. We will do our best to address these problems as fast and efficiently as possible.

# Authors

* Matthew Peres Tino
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz

"""