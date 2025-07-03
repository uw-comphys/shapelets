# Custom Commands

The shapelets library makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
Entry points are custom command-line arguments to use the shapelets package.

* `shapelets-run /path/to/config`
    * Purpose: To run shapelets analysis via configuration files 
    * Args: `/path/to/config` is the relative or absolute filepath to your configuration file - see the [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html)


* `shapelets-test`
    * Purpose: Triggers all shapelets unit tests. Use after modifying source code or to check your shapelets installation.