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

The shapelets package makes use of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
These are custom command-line arguments that trigger specific programming tasks in the background.

* `shapelets CONFIG` - here, `CONFIG` is the name of the text-based configuration file that will perform some specific analysis based on the parameters present in the file. See the package [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html).
* `shapelets-test` - triggers all unit tests in the [tests](https://github.com/uw-comphys/shapelets/tree/main/tests) directory and will report any failures. It is encouraged to use this command if modifying the package source code and after initially [installing](https://uw-comphys.github.io/shapelets/shapelets/docs/installation_guide.html) the `shapelets` package.

"""
