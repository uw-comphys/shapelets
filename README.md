## What is `shapelets`?

[**Summary**](#summary)
| [**Installation**](#installation-instructions)
| [**Examples**](#examples-of-usage)
| [**Authors**](#authors)


## Summary 

`Shapelets` is a python package that implements several shapelet functions and some of their significant applications in science and astronomy. These functions form a complete and orthonormal set, allowing them to capture complex geometries and information from any physical shape. Furthermore, shapelets are localized and can be scaled to match that of any physical feature. 

Due to these properties, they have seen extensive use in recent years, with several different formulations and applications, including

* Astronomy/astrophysics [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [L. Lentati (2015)](https://doi.org/10.48550/arXiv.1412.1427), [S. Birrer (2015)](https://doi.org/10.48550/arXiv.1504.07629), [G. Desvignes (2016)](https://doi.org/10.48550/arXiv.1602.08511), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837)], 
* Self-assembly materials [[R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)], 
* Computational neuroscience [[J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5)], and 
* Medical imaging [[J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760)].

In particular, the `shapelets` package provides documentation and code for four different shapelet functions: 

* Cartesian shapelets [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)], 
* Polar shapelets [[R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)],
* Orthonormal polar shapelets with constant radial scale [[T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353)], and 
* Exponential shapelets [[J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837)]. 

Applications implemented in the package include those from astronomy (galactic image decomposition and reconstruction) [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)] and shapelet-based methods to quantify order from self-assembly nanostructured surface imaging [[R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)]. 


## Getting Started

### Installation Instructions

To install `shapelets`, you should clone the repository onto your machine in the desired directory. This can be done using the Github GUI, but for simplicity it is preferred to use your terminal / command line interface, outlined below.

1. In your desired directory, type `git clone https://github.com/uw-comphys/shapelets.git`
2. Ensure that `pip3` is installed,
    * Linux - `sudo apt install python3-pip`
    * macOS - install [Homebrew](https://brew.sh/) via terminal. Then `brew install python3`, which also installs `pip3`
    * Windows - we recommend using WSL (Windows Subsystem for Linux), please follow [**here**](#installing-shapelets-on-wsl-windows-subsystem-for-linux) before proceeding
3. To install the `shapelets` package, type `pip3 install .` from the topmost package directory (i.e., /home/.../shapelets) 
4. To ensure correct installation, type `shapelets-test`, which should trigger the [custom command](#custom-commands) to initiate unit testing.

### Installing `shapelets` on WSL (Windows Subsystem for Linux)

For Windows users, we recommend using WSL (Windows Subsystem for Linux) which can easily be installed through the Microsoft Store. Please install Ubuntu 22.04 LTS. Additionally, Python 3.7+ should come pre-installed with WSL. Check this via `python3 --version`.

To be able to use the [custom commands](#custom-commands) developed for `shapelets` (also known as entry points), please perform the following steps.

* In your WSL terminal, type `nano ~/.bashrc`
* At the bottom of the file, append the following line `export PATH="/home/user/.local/bin:$PATH"` where `user` is the username of your WSL unix profile
* Press `CTRL+S` then `CTRL+X` to exit the editor
* Close your WSL terminal and restart the Ubuntu 22.04 LTS application


### Custom Commands

The `shapelets` package makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/). In brief, these are custom command line arguments that trigger specific functions for the `shapelets` package.

The entry points currently developed for `shapelets` are,

* `shapelets config` - here, 'config' is the name of the configuration file that executes specific methods or applications that are described by the parameters set in this file. Please see [interface methods](#interface-methods) and [example documentation](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) for more details.
* `shapelets-test` - this triggers all unit tests developed in the [tests](https://github.com/uw-comphys/shapelets) directory and will report any failures. It is encouraged to use this command if making any additions to the package codebase or installing the package for the first time.


### Interface Methods

The `shapelets` package can be used in two different formats, but users are encouraged to see the examples [examples](https://github.com/uw-comphys/shapelets/tree/main/examples) and related [documentation](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) to understand how to use both formats.

In brief, the two formats are:

1. Configuration file method - `shapelets` takes advantage of configuration files which provide a very simple platform to use the applications implemented. The central idea is that parameters are described in a plaintext file, wherein the code will read these parameters and execute necessary methods in the background. This format is intended for those unfamiliar with programming.
2. Scripting method - as with any python package, `shapelets` can be used in a more traditional format (importing relevant submodules in scripts). 


## Examples of Usage

Several in-depth examples were developed that explore the use and capabilities of the shapelets package for both astronomy and self-assembly related applications. All examples can be found [**here**](https://github.com/uw-comphys/shapelets/tree/main/examples) with documentation for the examples found [**here**](https://github.com/uw-comphys/shapelets/tree/main/docs/examples). The examples should be the first place for new users to understand how to use the shapelets package. All examples have instructions to use the `shapelets` package via both [**interface methods**](#interface-methods).

* Examples 1-3 demonstrate use of the `shapelets.self_assembly` submodule to compute relevant methods such as the response distance method ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307)), local pattern orientation ([M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)) and defect identification method ([M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)).
* Example 4 demonstrates use of the `shapelets.astronomy` submodule to compute the decomposition and reconstruction of galactic images [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)].


## Bug Tracking

If you encounter any **bugs** or **problems** with `shapelets`, please create a post using [Github's Issue Tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images or code-snippets where appropriate. We will do our best to address these problems as fast and efficiently as possible.


## Authors

`shapelets` package authors include,

* Matthew Peres Tino 
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz
