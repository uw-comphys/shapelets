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

# Installation Instructions

shapelets is available on all operating systems via Python's main package manager, pip. 
Please ensure that Python 3.10+ is installed on your machine. If you do not have Python installed, see [here](#installing-python).

If Python is installed on your machine, type `pip install shapelets` into your terminal/command line to install the shapelets package. 
New users are also encouraged to visit the [official website](https://uw-comphys.github.io/shapelets/shapelets.html) to understand how the shapelets package can be used along with detailed examples, custom terminal commands provided by the package, and more. 

## Installing Python

### Windows

1. Download Python 3.10+ from the [official website](https://www.python.org/) or from the Microsoft Store
2. Open Command Prompt, and install the shapelets package via: `pip install shapelets`
3. Optionally, after successful installation, you can verify the integrity of the shapelets package via: `shapelets-test`

### Mac OS

Please ensure your macOS is at least macOS 12 Monterey (released 2021).

1. Install [Homebrew](https://brew.sh/) by copy and pasting the link on their homepage into your terminal
2. Install Python 3.10 and pip via: `brew install python@3.10` (automatically installs pip) 
3. Install the shapelets package via `pip install shapelets`
4. Optionally, after successful installation, you can verify the integrity of the shapelets package via: `shapelets-test`

### Linux

1. For debian based distributions (i.e. Ubuntu), update your system via: `sudo apt-get update`
2. Install Python 3.10 and pip via: `sudo apt-get install python3.10 python3-pip`
3. Install the shapelets package via: `pip install shapelets`
4. Optionally, after successful installation, you can verify the integrity of the shapelets package via: `shapelets-test`

"""