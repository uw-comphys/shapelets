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

# Custom Commands

The shapelets library makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
These are custom command-line arguments that trigger specific library actions.

* `shapelets CONFIG` - this entry point is used to interact with the shapelets library via configuration files. Here `CONFIG` is the name of the text-based configuration file that details specific parameters for an analysis. See the library [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html) for useful demonstration. 
* `shapelets-test` - triggers all library [unit tests](https://github.com/uw-comphys/shapelets/tree/main/shapelets/tests) and will report any failures. It is encouraged to use this command if (1) you are modifying the library source code or (2) after initial library [installation](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html).

"""
