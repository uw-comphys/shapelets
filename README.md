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


## Installation Instructions

Installing `shapelets` highly depends on the OS of your machine. Please follow the appropriate guide depending on your OS (Linux, Mac OS, Windows). 

### Linux

1. Update your Ubuntu system via `sudo apt-get update`
2. Install `git`, `python3`, and `pip` via `sudo apt-get install git python3 python3-pip`
3. Clone the `shapelets` repository via `git clone https://github.com/uw-comphys/shapelets.git`
4. To install `shapelets`, navigate to your /shapelets directory, then type `pip3 install .`
5. To ensure correct installation, type `shapelets-test`, which should trigger the [custom command](#custom-commands) to initiate unit testing

### Mac OS

1. Install [Homebrew](https://brew.sh/); it is an amazing package manager that will make this process easier
2. Install `git`, `python3`, and `pip` via `brew install python3` (which also installs pip) then `brew install git`
3. Clone the `shapelets` repository via `git clone https://github.com/uw-comphys/shapelets.git`
4. To install `shapelets`, navigate to your /shapelets directory, then type `pip3 install .`
5. To ensure correct installation, type `shapelets-test`, which should trigger the [custom command](#custom-commands) to initiate unit testing 

### Windows

For Windows users, we **strongly** recommend using WSL (Windows Subsystem for Linux). Please follow the steps below.

1. Install Ubuntu 22.04 LTS from the Microsoft Store
2. Open Ubuntu 22.04 LTS and create a Unix profile (username and password) 
3. Enter `sudo apt-get update` into your terminal to get the most recent Ubuntu updates
4. Install `git`, `python3`, and `pip` via `sudo apt-get install git python3 python3-pip`
5. Install a graphics library needed to use `openCV` for `shapelets` via `sudo apt-get install libgl1-mesa-glx`
5. Clone the `shapelets` repository via `git clone https://github.com/uw-comphys/shapelets.git`
6. To install `shapelets`, navigate to your /shapelets directory, then type `pip3 install .`
    * Note: to locate where your Ubuntu directories are stored, type `explorer.exe .` into the terminal, and your Windows explorer will open with the correct path to your Ubuntu system
    * You can pin this address to your system by clicking *File* then *Pin to Quick Access*
7. To be able to use the [custom commands](#custom-commands) developed for `shapelets`, please follow the instructions [**here**](#editing-path-to-use-shapelets-custom-commands)
8. To allow graphics support for Ubuntu, follow the instructions [**here**](#graphics-correction-for-windows-users-via-ubuntu--wsl) 
9. To ensure correct installation, type `shapelets-test`, which should trigger the [custom command](#custom-commands) to initiate unit testing


## Custom Commands

The `shapelets` package makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/). In brief, these are custom command line arguments that trigger specific functions for the `shapelets` package.

The entry points currently developed for `shapelets` are,

* `shapelets config` - here, 'config' is the name of the configuration file that executes specific methods or applications that are described by the parameters set in this file. Please see [Methods of Usage](#methods-of-usage) and [example documentation](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) for more details.
* `shapelets-test` - this triggers all unit tests developed in the [tests](https://github.com/uw-comphys/shapelets) directory and will report any failures. It is encouraged to use this command if making any additions to the package codebase or installing the package for the first time.


## Methods of Usage

The `shapelets` package can be used in two different formats, but users are encouraged to see the examples [examples](https://github.com/uw-comphys/shapelets/tree/main/examples) and related [documentation](https://github.com/uw-comphys/shapelets/tree/main/docs/examples) to understand how to use both formats.

In brief, the two formats are:

1. Configuration file method - `shapelets` takes advantage of configuration files which provide a very simple platform to use the applications implemented. The central idea is that parameters are described in a plaintext file, wherein the code will read these parameters and execute necessary methods in the background. This format is intended for those unfamiliar with programming.
2. Scripting method - as with any python package, `shapelets` can be used in a more traditional format (importing relevant submodules in scripts). 


## Examples of Usage

Several in-depth examples were developed that explore the use and capabilities of the shapelets package for both astronomy and self-assembly related applications. All examples can be found [**here**](https://github.com/uw-comphys/shapelets/tree/main/examples) with documentation for the examples found [**here**](https://github.com/uw-comphys/shapelets/tree/main/docs/examples). The examples should be the first place for new users to understand how to use the shapelets package. All examples have instructions to use the `shapelets` package via both [**Methods of Usage**](#methods-of-usage).

* Examples 1-3 demonstrate use of the `shapelets.self_assembly` submodule to compute relevant methods such as the response distance method ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307)), local pattern orientation ([M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)) and defect identification method ([M. P. Tino (in revision)](https://github.com/uw-comphys/shapelets)).
* Example 4 demonstrates use of the `shapelets.astronomy` submodule to compute the decomposition and reconstruction of galactic images [[A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)].


## WSL (Windows Subsystem for Linux) Additional Installation Steps

### Editing PATH to use `shapelets` [Custom Commands](#custom-commands)

**Note**: this is for WSL users only.

1. In your Ubuntu terminal, type `cd` then `vim .bashrc`
2. Press `i` to enter *insert mode*, which will allow you to edit the file
3. Use the arrow keys to navigate to the bottom of the file, then add the line `export PATH="/home/user/.local/bin:$PATH"` where `user` is the username of your Ubuntu unix profile
4. Press `ESC` then type `:wq` to *write* your changes and *quit* from the VIM editor
5. Restart the Ubuntu 22.04 LTS application (close and re-open)

### Graphics Correction for Windows users via Ubuntu & WSL

**Note**: this is for WSL users only. 

Unfortunately, Ubuntu via WSL does not come with GUI (graphical user interface) application support (shortformed an "X server"). In order to view output plots or any graphical interface (such as `matplotlib`), please follow the following.

1. In your Ubuntu terminal, type `sudo apt-get install ubuntu-desktop`
2. Change your environment display variables,
    * In your Ubuntu terminal, type `cd` then `vim .bashrc`
    * Press `i` to enter *insert mode*, which will allow you to edit the file
    * Use the arrow keys to navigate to the bottom of the file, then add the line `export DISPLAY=$(ip route list default | awk '{print $3}'):0`
    * On a new line, add `export LIBGL_ALWAYS_INDIRECT=1`
    * Press `ESC` then type `:wq` to *write* your changes and *quit* from the VIM editor
    * Restart the Ubuntu 22.04 LTS application (close and re-open)
3. Enable Public Access on your X11 server for Windows. Follow this [tutorial](https://skeptric.com/wsl2-xserver/) but be sure to only follow the section labelled *Allow WSL Access via Windows Firewall*
4. Download [VcXsrv](https://sourceforge.net/projects/vcxsrv/). 
    * On your Windows machine (not Ubuntu), navigate to `C:\Program Files\VcXsrv` and open the application`xlaunch.exe`
    * Click Next until you reach the *Extra Settings* page. Check the box for *Disable Access Control*
    * Save the configuration file somewhere useful. Ensure that you run the `config.xlaunch` file before executing code with any graphical interface or support


## Bug Tracking

If you encounter any **bugs** or **problems** with `shapelets`, please create a post using [Github's Issue Tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images or code-snippets where appropriate. We will do our best to address these problems as fast and efficiently as possible.


## Authors

`shapelets` package authors include,

* Matthew Peres Tino 
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz
