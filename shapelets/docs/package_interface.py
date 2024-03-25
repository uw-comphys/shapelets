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

# Package Interfacing

The `shapelets` package can be interfaced in two different ways:

1. Configuration file method (developed for non-programmers)
    * Parameters are described in a text-based configuration file, and the `shapelets` package then reads this file and runs the appropriate analysis
2. Scripting method (intended for those comfortable with Python programming)
    * A more traditional format where relevant methods are imported in python files, i.e. 

```python 
from shapelets.functions import cartesian2D
```

The [examples](https://uw-comphys.github.io/shapelets/shapelets/docs.html) are implemented primarily using the text-based configuration file method (#1).
However, the examples also have Python files (.py) that perform the exact same analysis as shown via the configuration file method. 

"""
