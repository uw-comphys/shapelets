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

"""
The self-assembly submodule.
"""

import warnings

# Allow for easy access to main self-assembly applications
# e.g. from shapelets.self_assembly import response_distance
from shapelets.self_assembly.apps import(
    response_distance,
    identify_defects,
    orientation,
)

def __getattr__(name):
    r"""Handle deprecated function names with import-time warnings."""
    
    defunct = {
        'rdistance': response_distance,
        'defectid': identify_defects
    }

    if name in defunct:
        warnings.warn(
            f"{name}() is deprecated, please use {defunct[name].__name__}() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return defunct[name]
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")