# shapelets

[![DOI](https://joss.theoj.org/papers/10.21105/joss.06058/status.svg)](https://doi.org/10.21105/joss.06058)

[**Getting Started**](#getting-started)
| [**Issues**](#issues)
| [**Contribute**](#contribute)
| [**Citation**](#citation)
| [**Authors**](#authors)

## What is shapelets? 

Shapelets is a Python library that implements several shapelet functions and some of their applications in science and engineering. Shapelet functions are a complete and orthogonal set of localized basis functions with mathematical properties convenient for image analysis and manipulation. Applications of shapelet functions include

* Astronomy/astrophysics ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837)),
* Nanostructure characterization ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)),
* Computational neuroscience ([J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5)), and
* Medical imaging ([J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760))

The shapelets library provides reference code and documentation for several shapelet function definitions, including

* Cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)), 
* Polar shapelets ([R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445)),
* Exponential shapelets ([J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837)),
* Orthonormal polar shapelets with no radial symmetry ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353)), and 
* Orthonormal polar shapelets with one degree of radial symmetry ([M. P. Tino (2024)](https://hdl.handle.net/10012/20779))

## Getting Started

If you have Python 3.10+ installed on your machine, you can install the shapelets library in the terminal via pip: `pip install shapelets`

Otherwise, consult the [official website](https://uw-comphys.github.io/shapelets/shapelets.html) for installation instructions, detailed examples, and custom command-line arguments to interact with the shapelets library efficiently.

## Issues

If you encounter any **bugs** or **problems** with shapelets, please create a post using the library [issue tracker](https://github.com/uw-comphys/shapelets/issues). Please provide a clear and concise description of the problem, with images/code-snippets where appropriate. We will address these problems as fast as possible.

## Contribute

The authors of the shapelets library welcome external contributions to the source code. This process will be easiest if users adhere to the contribution policy:

* Open an issue on the library [issue tracker](https://github.com/uw-comphys/shapelets/issues) clearly describing your intentions on code modifications or additions
* Ensure your modifications or additions adhere to the existing standard of the shapelets library, specifically detailed docstring formatting for new methods
* Test your modifications to ensure that the core functionality of the library has not been altered by running the unit tests via the entry point: `shapelets-test`
* Once the issue has been discussed with a library author, you may open a pull request containing your code modifications

## Citation

If you plan to use shapelets in your own work, please cite using the *Cite this repository* dropdown button on the top right of this page (under *About*).

## Authors

* Matthew Peres Tino (mptino@uwaterloo.ca)
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz
