# Custom Commands

The shapelets library makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
Entry points are custom command-line arguments to use the shapelets package.

* `shapelets-run /path/to/config`
    * To run shapelets analysis via configuration files 
    * Here `/path/to/config` is the relative or absolute filepath to your configuration file - see the [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html)

* `shapelets-test`
    * Triggers all shapelets unit tests. 
    * You should use this command after modifying the source code or to confirm successful installation of the shapelets package