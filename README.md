## What is `shapelets`?

[**Summary**](#summary)
| [**Installation**](#installation)
| [**Examples**](#examples-of-usage)
| [**Contribute**](#contribute)
| [**Issues**](#issues)
| [**Authors**](#authors)


## Summary 

`Shapelets` is a python package that implements several shapelet functions and some of their significant applications in science and astronomy. These functions form a complete and orthonormal set, allowing them to capture complex geometries and information from any physical shape. Furthermore, shapelets are localized and can be scaled to match that of any physical feature. 

Due to these properties, they have seen extensive use in recent years, with several different formulations and applications:

* Astronomy/astrophysics ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))
* Nanomaterials ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (accepted)](https://github.com/uw-comphys/shapelets))
* Computational neuroscience ([J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5))
* Medical imaging ([J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760))

The `shapelets` package provides reference documentation and code for four (4) shapelet functions: 

* Cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)), 
* Polar shapelets ([R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)),
* Orthonormal polar shapelets with constant radial scale ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353)), and 
* Exponential shapelets ([J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))


## Installation

Installing `shapelets` is highly dependent on the operating system of your machine. Package is currently compatible with Python 3.10.

### Mac OS

Please ensure your macOS is at least macOS 12 Monterey (released 2021).

1. Install [Homebrew](https://brew.sh/) by copy and pasting the command website homepage into your terminal
2. Install `git`, `python3.10`, and `pip` in the terminal: `brew install git python@3.10` (automatically installs pip) 
3. Clone this repository: `git clone https://github.com/uw-comphys/shapelets.git`
4. Navigate to the top-most directory (i.e. ./shapelets) and install this package: `pip3.10 install .`
5. Ensure correct installation by running unit tests via the [custom command](#custom-commands): `shapelets-test`

### Windows

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
8. Follow the [enable custom commands](https://github.com/uw-comphys/shapelets/tree/main/docs/WSL) instructions to allow use of package [custom commands](#custom-commands) 
9. Ensure correct installation by running unit tests via the [custom command](#custom-commands): `shapelets-test`

**Note** - if this is your first time installing Ubuntu on WSL, you may need to follow the [enable graphics](https://github.com/uw-comphys/shapelets/tree/main/docs/WSL) instructions to allow graphics support (i.e. figures from `matplotlib`).

### Linux

1. Update your Ubuntu system: `sudo apt-get update`
2. Install `git`, `python3.10`, and `pip`: `sudo apt-get install git python3.10 python3-pip`
3. Clone the repository: `git clone https://github.com/uw-comphys/shapelets.git`
4. Navigate to the top-most directory (i.e. ./shapelets) and install this package: `pip3 install .`
5. Ensure correct installation by running unit tests via the [custom command](#custom-commands): `shapelets-test`


## Custom Commands

The `shapelets` package makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/), which are custom command line arguments that trigger specific tasks.

* `shapelets CONFIG` - here, `CONFIG` is the name of the plaintext configuration file that will run specific package methods based on the parameters listed in the file
* `shapelets-test` - triggers all unit tests in the [tests](https://github.com/uw-comphys/shapelets) directory and will report any failures. It is encouraged to use this command if modifying the package source code and after initial package [installation](#installation)


## Examples of Usage

The `shapelets` package can be used in two different formats.

1. Configuration file method (developed for non-programmers)
    * Parameters are described in a plaintext file, and the code then reads these parameters and runs the relevant code in the background
2. Scripting method (intended for programmers)
    * A more traditional format where relevant methods are imported in python files, i.e. 
    ```python 
    from shapelets.functions import cartesian2D
    ```

Several in-depth examples (using both formats described above) were developed that showcase the applications of the `shapelets` package. 
The [examples](https://github.com/uw-comphys/shapelets/tree/main/examples) and related [documentation](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) should be explored by all new users.

* Examples 1-3 use the `shapelets.self_assembly` sub-module to quantify order from microscopy images of materials (namely those from self-assembly):
    * The response distance method ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307))
    * Local pattern orientation ([M. P. Tino (accepted)](https://github.com/uw-comphys/shapelets))
    * Defect identification method ([M. P. Tino (accepted)](https://github.com/uw-comphys/shapelets))
* Example 4 uses the `shapelets.astronomy` sub-module:
    * Galaxy decomposition and reconstruction [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)]


## Contribute

The authors of the `shapelets` package welcome external contributions to the source code. This process will be easiest if users adhere to the contribution policy:

* Open an issue on the package [issue tracker](https://github.com/uw-comphys/shapelets/issues) clearly describing your intentions on code modifications or additions
* Ensure your modifications or additions adhere to the existing standard of the `shapelets` package, specifically detailed documentation for new methods (see existing methods for example documentation)
* Test your modifications to ensure that the core functionality of the package has not been altered by running the unit tests via the custom command: `shapelets-test`
* Once the issue has been discussed with a package author, you may open a pull request containing your modifications


## Issues

If you encounter any **bugs** or **problems** with `shapelets`, please create a post using our package [issue tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images or code-snippets where appropriate. We will do our best to address these problems as fast and efficiently as possible.


## Authors

`shapelets` package authors:

* Matthew Peres Tino
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz
