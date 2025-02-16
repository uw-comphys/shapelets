########################################################################################################################
# Copyright 2023 the authors (see AUTHORS file for full list).                                                         #
#                                                                                                                      #
# This file is part of shapelets.                                                                                      #
#                                                                                                                      #
# Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General       #
# Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)  #
# any later version.                                                                                                   #
#                                                                                                                      #
# Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied      #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see           #
# <https://www.gnu.org/licenses/>.                                                                                     #
########################################################################################################################

r"""

# Custom Commands (entry points)

The shapelets library makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
These are custom command-line arguments to interact with the shapelets package.

* `shapelets-run /path/to/config` - To run a shapelets application via configuration file. Here `/path/to/config` is the relative or absolute filepath to your configuration file - see the [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html). 
* `shapelets-test` - triggers all shapelets unit tests. Use this command either (1) after modifying the source code or (2) after [installation](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html) to ensure library integrity.

"""
