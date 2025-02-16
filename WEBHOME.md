[![DOI](https://joss.theoj.org/papers/10.21105/joss.06058/status.svg)](https://doi.org/10.21105/joss.06058)

## What is shapelets? 

Shapelets is a Python library that implements several shapelet functions and some of their applications in science and engineering. Shapelet functions are a complete and orthogonal set of localized basis functions with mathematical properties convenient for various image analyses. Existing applications from the literature include:

* Astronomy/astrophysics ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x), [R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445), [J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))
* Nanostructure characterization ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307), [T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353), [M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4))
* Computational neuroscience ([J. D. Victor (2006)](https://doi.org/10.1152/jn.00498.2005), [T. O. Sharpee (2009)](https://doi.org/10.1007%2Fs10827-008-0107-5))
* Medical imaging ([J. Weissman (2004)](https://doi.org/10.1364/OPEX.12.005760))

## Main features

Shapelets provides implementations of the following shapelet functions from ``shapelets.core.functions``

* Cartesian shapelets ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)) 
* Polar shapelets ([R. Massey (2005)](https://doi.org/10.48550/arXiv.astro-ph/0408445))
* Exponential shapelets ([J. Berge (2019)](https://doi.org/10.48550/arXiv.1903.05837))
* Orthonormal polar shapelets with no radial extrema ([T. Akdeniz (2018)](https://doi.org/10.1088/1361-6528/aaf353))
* Orthonormal polar shapelets with one degree of radial extrema ([M. P. Tino (2024)](https://hdl.handle.net/10012/20779))

It also implements several shapelets applications, such as
* The response distance method ([R. Suderman (2015)](http://dx.doi.org/10.1103/PhysRevE.91.033307)) - see [example 1](https://uw-comphys.github.io/shapelets/shapelets/docs/example_1.html)
* The defect identification method ([M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) - see [example 2](https://uw-comphys.github.io/shapelets/shapelets/docs/example_2.html)
* The local pattern orientation method ([M. P. Tino (2024)](http://dx.doi.org/10.1088/1361-6528/ad1df4)) - see [example 3](https://uw-comphys.github.io/shapelets/shapelets/docs/example_3.html)
* Galaxy decomposition and reconstruction ([A. Refregier (2003)](https://doi.org/10.1046/j.1365-8711.2003.05901.x)) - see [example 4](https://uw-comphys.github.io/shapelets/shapelets/docs/example_4.html)

## Getting Started

If you have Python 3.10+ installed, you can install the shapelets library via pip:
```
pip install shapelets
```
If you do not have Python 3.10+ installed, consult the [installation guide](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html). Be sure to also checkout the [custom commands](https://uw-comphys.github.io/shapelets/shapelets/docs/custom_commands.html) and [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html) to see which shapelets applications are implemented and how to interact with the shapelets library.

If you plan to use the shapelets library for your own work, please cite appropriately using this [citation](#citation).
For any problems, create a post using the [issue tracker](https://github.com/uw-comphys/shapelets/issues). 

## Contribute

The authors of the shapelets library welcome contributions to the source code. 
Please follow the contribution policy [here](https://github.com/uw-comphys/shapelets/blob/main/CONTRIBUTE.md).

## Citation
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

* Matthew Peres Tino (mptino@uwaterloo.ca)
* Abbas Yusuf Abdulaziz 
* Nasser Mohieddin Abukhdeir
* Robert Suderman 
* Thomas Akdeniz