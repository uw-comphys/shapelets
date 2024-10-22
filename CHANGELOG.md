# Changelog
All substantial or important changes to `shapelets` will be written in this file, with each release containing its changes in reverse chronological order.

## Commit Message Index
- FIX: Fix for current bug(s), with reference to [GitHub issues](https://github.com/uw-comphys/shapelets/issues) when possible 
- LOG: Modifications to CHANGELOG for version control documentation
- MNT: General modifications, maintenance (including documentation), or enhancements 
- NEW: Introduction of a new component or feature

## UNRELEASED
- NEW: Introduced CHANGELOG.md for detailed version control history 
- NEW: Introduced `shapelets.core` for essential components (i.e., shapelet functions, entry points)
- FIX: Corrected characteristic wavelength overestimation ([#64](https://github.com/uw-comphys/shapelets/pull/64))
- FIX: Corrected optimal filter orientation for steerable shapelets ([#62](https://github.com/uw-comphys/shapelets/pull/62)) 
- MNT: Several documentation changes, including fixes for pdoc website compilation errors 
- NEW: Added orthonormal (n=1) polar shapelets, with supporting methods and unit tests 
- FIX: Fixed entry point bug using incorrect python interpreter from local machine ([#55](https://github.com/uw-comphys/shapelets/pull/55))
- MNT: Merged setup.cfg and MANIFEST.in into pyproject.toml, which now holds all project specifications
- MNT: Replaced existing Python response distance with C++ implementation, achieving ~15x speed-up!

## [1.1] -- 12/04/2024
- commit cd45ff9174503c44179538af2d83cf2c2444d53a
- FIX: Fixed issue where unit tests were not available after pip installation ([#45](https://github.com/uw-comphys/shapelets/pull/45))
- MNT: Simplified input parameters and improved readability for `shapelets.self_assembly` methods 
- MNT: Edits to documentation, including examples, README, and official website
- NEW: Formal library citation now available via CITATION.cff
- MNT: Minor modifications and corrections to [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058)

## [1.0] -- 03/14/2024
- commit 6ce31fbd1194cac024f1f65d2fa7c21ed0c67990
- NEW: Initial complete and functional release following [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058) acceptance