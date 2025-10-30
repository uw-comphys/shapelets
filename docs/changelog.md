# Changelog
All substantial or important changes to `shapelets` will be written in this file, with each release containing its changes in reverse chronological order.

## Commit Message Index
- FIX: Fix for current bug(s) or potential issues
- LOG: Modifications to CHANGELOG for version control documentation
- MNT: General modifications, maintenance (including documentation), or enhancements 
- NEW: Introduction of a new component, feature, or capability

## [1.3] -- Oct 27, 2025
- FIX: Restored original importing schemes to match JOSS paper, ([#83](https://github.com/uw-comphys/shapelets/pull/83))
- MNT: Deprecated function warnings for old function imports (from JOSS paper) ([#83](https://github.com/uw-comphys/shapelets/pull/83))
- MNT: Exclude `shapelets/docs` from `pip install` ([#82](https://github.com/uw-comphys/shapelets/pull/82))
- MNT: Documentation maintenance; removed `pdoc` as dependency ([#81](https://github.com/uw-comphys/shapelets/pull/81))
- NEW: New GitHub actions to run unit-tests on multiple OS platforms ([#80](https://github.com/uw-comphys/shapelets/pull/80))
- NEW: Enforced `numpy` docstring format for all functions ([#77](https://github.com/uw-comphys/shapelets/pull/77))
- NEW: Added CC as latest author to shapelets package, welcome! ([#77](https://github.com/uw-comphys/shapelets/pull/77))
- MNT: Support for passing relative/absolute filepaths to config file, e.g. `shapelets-run /path/to/config` ([#76](https://github.com/uw-comphys/shapelets/pull/76))
- MNT: Change main entry point from `shapelets` to `shapelets-run` ([#76](https://github.com/uw-comphys/shapelets/pull/76))
- NEW: Addition of source unsupervised shapelet technique via `auto.py` (not release) ([#73](https://github.com/uw-comphys/shapelets/pull/73))

## [1.2] -- Dec 14, 2024
- NEW: Introduced CHANGELOG.md for detailed version control history ([#69](https://github.com/uw-comphys/shapelets/pull/69))
- NEW: Introduced `shapelets.core` for essential components ([#68](https://github.com/uw-comphys/shapelets/pull/68))
- FIX: Technical shapelets fixes, see PRs ([#62](https://github.com/uw-comphys/shapelets/pull/62)), ([#64](https://github.com/uw-comphys/shapelets/pull/64))
- MNT: Several documentation changes, such as fixes for pdoc website compilation errors  
- NEW: Added orthonormal (n=1) polar shapelets framework and unit tests ([#56](https://github.com/uw-comphys/shapelets/pull/56))
- FIX: Fixed entry point bug using incorrect python interpreter from local machine ([#55](https://github.com/uw-comphys/shapelets/pull/55))
- MNT: Merged setup.cfg and MANIFEST.in into pyproject.toml ([#55](https://github.com/uw-comphys/shapelets/pull/55))
- MNT: Replaced Python response distance implementation with C++, ~15x speed-up! ([#48](https://github.com/uw-comphys/shapelets/pull/48))

## [1.1] -- Apr 12, 2024
- FIX: Fixed issue where unit tests were not available after pip installation ([#45](https://github.com/uw-comphys/shapelets/pull/45))
- MNT: Simplified input parameters and improved readability for `shapelets.self_assembly` methods 
- MNT: Edits to documentation, including examples, README, and official website
- NEW: Formal library citation now available via CITATION.cff 
- MNT: Minor modifications and corrections to [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058)

## [1.0] -- Mar 14, 2024
- NEW: Initial complete and functional release following [JOSS manuscript](https://joss.theoj.org/papers/10.21105/joss.06058) acceptance