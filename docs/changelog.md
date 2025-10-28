# Changelog
All substantial or important changes to `shapelets` will be written in this file, with each release containing its changes in reverse chronological order.

## Commit Message Index
- FIX: Fix for current bug(s), with reference to [GitHub issues](https://github.com/uw-comphys/shapelets/issues) when possible 
- LOG: Modifications to CHANGELOG for version control documentation
- MNT: General modifications, maintenance (including documentation), or enhancements 
- NEW: Introduction of a new component or feature

## [1.3] -- Oct 27, 2025
- FIX: Restored original importing schemes to match JOSS paper, e.g. `from shapelets.self_assembly import orientation` ([#83](https://github.com/uw-comphys/shapelets/pull/83))
- MNT: Deprecated function warnings; old imports (from JOSS paper) will still work, user notified of new function name ([#83](https://github.com/uw-comphys/shapelets/pull/83))
- MNT: Exclude `shapelets/docs` from `pip install` ([#82](https://github.com/uw-comphys/shapelets/pull/82))
- MNT: Documentation maintenance and removed `pdoc` as dependency ([#81](https://github.com/uw-comphys/shapelets/pull/81))
- MNT: Modify GitHub action for JOSS paper compilation to run only on `publications` branch ([#80](https://github.com/uw-comphys/shapelets/pull/80))
- NEW: New GitHub actions to run unit-tests on windows, macos, and linux (ubuntu) ([#80](https://github.com/uw-comphys/shapelets/pull/80))
- NEW: Enforced `numpy` docstring format for all functions ([#77](https://github.com/uw-comphys/shapelets/pull/77))
- NEW: Added CC as latest author to shapelets package, welcome! ([#77](https://github.com/uw-comphys/shapelets/pull/77))
- MNT: Support for passing relative/absolute filepaths to config file, e.g. `shapelets-run /path/to/config` ([#76](https://github.com/uw-comphys/shapelets/pull/76))
- MNT: Change main entry point from `shapelets` to `shapelets-run` ([#76](https://github.com/uw-comphys/shapelets/pull/76))
- NEW: Addition of unsupervised shapelet method via `auto.py` (is standalone script; needs work to merge into package) ([#73](https://github.com/uw-comphys/shapelets/pull/73))

## [1.2] -- Dec 14, 2024
- NEW: Introduced CHANGELOG.md for detailed version control history 
- NEW: Introduced `shapelets.core` for essential components (i.e., shapelet functions, entry points) ([#68](https://github.com/uw-comphys/shapelets/pull/68))
- FIX: Corrected characteristic wavelength overestimation ([#64](https://github.com/uw-comphys/shapelets/pull/64))
- FIX: Corrected optimal filter orientation for steerable shapelets ([#62](https://github.com/uw-comphys/shapelets/pull/62)) 
- MNT: Several documentation changes, including fixes for pdoc website compilation errors  
- NEW: Added orthonormal (n=1) polar shapelets, with supporting methods and unit tests ([#56](https://github.com/uw-comphys/shapelets/pull/56))
- FIX: Fixed entry point bug using incorrect python interpreter from local machine ([#55](https://github.com/uw-comphys/shapelets/pull/55))
- MNT: Merged setup.cfg and MANIFEST.in into pyproject.toml, which now holds all project specifications ([#55](https://github.com/uw-comphys/shapelets/pull/55))
- MNT: Replaced existing Python response distance with C++ implementation, achieving ~15x speed-up! ([#48](https://github.com/uw-comphys/shapelets/pull/48))

## [1.1] -- Apr 12, 2024
- FIX: Fixed issue where unit tests were not available after pip installation ([#45](https://github.com/uw-comphys/shapelets/pull/45))
- MNT: Simplified input parameters and improved readability for `shapelets.self_assembly` methods 
- MNT: Edits to documentation, including examples, README, and official website
- NEW: Formal library citation now available via CITATION.cff 
- MNT: Minor modifications and corrections to [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058)

## [1.0] -- Mar 14, 2024
- NEW: Initial complete and functional release following [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058) acceptance