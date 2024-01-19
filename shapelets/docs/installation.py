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

shapelets requires Python 3.10 or greater.
Installing shapelets is highly dependent on the operating system of your machine, be sure to follow the appropriate guidelines.

## Mac OS

Please ensure your macOS is at least macOS 12 Monterey (released 2021).

1. Install [Homebrew](https://brew.sh/) by copy and pasting the command website homepage into your terminal
2. Install `git`, `python3.10`, and `pip` in the terminal: `brew install git python@3.10` (automatically installs pip) 
3. Clone this repository: `git clone https://github.com/uw-comphys/shapelets.git`
4. Navigate to the top-most directory (i.e. ./shapelets) and install this package: `pip3.10 install .`
5. Ensure correct installation by running the unit tests [custom command](https://mptino.github.io/shapelets/shapelets/docs/usage.html) on the CLI: `shapelets-test`

## Windows

The instructions for Windows use WSL (Windows Subsystem for Linux). 

1. Install Ubuntu 22.04 LTS from the Microsoft Store 
2. Open Ubuntu 22.04 LTS and create a Unix profile (username and password) 
3. If the following error occurs: `WSLRegisterDistribution failed with error: 0x80370102`, follow these steps
	* Open *Turn Windows Features on and off*, and enable the following
	* *Virtual Machine Platform*, *Windows Subsystem for Linux*, and *Hyper-V* (if available) 
	* Restart your PC and return to step 2
4. Update your Ubuntu system:  `sudo apt-get update`
5. Install `git`, `python3.10`, `pip`, and a graphics library: `sudo apt-get install git python3.10 python3-pip libgl1-mesa-glx`
6. Clone the repository: `git clone https://github.com/uw-comphys/shapelets.git`
7. Navigate to the top-most directory (i.e. ./shapelets) and install this package: `pip3 install .`
8. Follow the [enable custom commands](https://mptino.github.io/shapelets/shapelets/docs/WSL.html) instructions to be able to use the package's [custom commands](https://mptino.github.io/shapelets/shapelets/docs/usage.html) 
9. Ensure correct installation by running the unit tests [custom command](https://mptino.github.io/shapelets/shapelets/docs/usage.html) on the CLI: `shapelets-test`

**Note** - if this is your first time installing Ubuntu on WSL, you may also need to follow the [enable graphics](https://mptino.github.io/shapelets/shapelets/docs/WSL.html) instructions to allow graphics support (i.e. figures from `matplotlib`).

## Linux

1. Update your Ubuntu system: `sudo apt-get update`
2. Install `git`, `python3.10`, and `pip`: `sudo apt-get install git python3.10 python3-pip`
3. Clone the repository: `git clone https://github.com/uw-comphys/shapelets.git`
4. Navigate to the top-most directory (i.e. ./shapelets) and install this package: `pip3 install .`
5. Ensure correct installation by running the unit tests [custom command](https://mptino.github.io/shapelets/shapelets/docs/usage.html) on the CLI: `shapelets-test`

"""