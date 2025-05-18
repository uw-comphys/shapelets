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
This module holds functions for kernel (filter) handling, such as making discrete grids and computing optimal kernel sizes.
"""

import numpy as np

from shapelets.functions import(
    orthonormalpolar2D_n0, 
    orthonormalpolar2D_n1
)

__all__ = [
    'make_grid',
    'get_opt_kernel_n0',
    'get_opt_kernel_n1',
]


def make_grid(N: int):
    r""" 
    Make discretized grid based on width (N).
    
    Parameters
    ----------
    * N: int
        * The width of the kernel (odd numbers only)

    Returns
    -------
    * grid_x: np.ndarray
        * The grid's x coordinate space
    * grid_y: np.ndarray
        * The grid's y coordinate space
    
    Notes
    -----
    As per convention, N should only be an odd number. Additionally, note that grid_x = grid_y.

    """
    if N % 2 == 0:
        print('Detected even grid size, adding 1 to enforce odd rule See self_assembly.wavelength.make_grid() docs.')
        N += 1
    if N < 9:
        raise ValueError('N must be at least 3 or greater.')
    
    bounds = [-(N-1)/2.0, (N-1)/2.0]
    grid = np.linspace(bounds[0], bounds[1], N)
    grid_x, grid_y = np.meshgrid(grid, grid)

    return grid_x, grid_y

def get_opt_kernel_n0(m: int, beta: float) -> np.ndarray:
    r""" 
    Determines the optimal filter (kernel) width for an $n=0$ orthonormal polar shapelet function [1] based on $\beta$, the shapelet length-scale parameter.
    
    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry
    * beta: float
        * The characteristic shapelet length scale parameter.
    
    Returns
    -------
    * shapelet: np.ndarray
        * Shapelet function casted onto a discrete domain with the appropriate filter width.

    References
    ----------
    * [1] https://doi.org/10.1088/1361-6528/aaf353

    """
    # start with small kernel size and scale up until satisfied
    N = 21 # minimum

    grid_x, grid_y = make_grid(N = N)
    shapelet = orthonormalpolar2D_n0(m=m, x1=grid_x, x2=grid_y, beta=beta)

    accept = False

    while not accept:
        edgeweight = np.abs(np.real(shapelet[int(shapelet.shape[0]/2), -1])) \
            / np.real(shapelet).max()
        if edgeweight > 0.0001:
            N += 4
            grid_x, grid_y = make_grid(N = N)
            shapelet = orthonormalpolar2D_n0(m=m, x1=grid_x, x2=grid_y, beta=beta)
        else:
            accept = True
    
    return shapelet

def get_opt_kernel_n1(m: int, beta: float) -> np.ndarray:
    r""" 
    Determines the optimal filter (kernel) width for an $n=1$ orthonormal polar shapelet function [1] based on $\beta$, the shapelet length-scale parameter.

    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry
    * beta: float
        * The characteristic shapelet length scale parameter.
    
    Returns
    -------
    * shapelet: np.ndarray
        * Shapelet function casted onto a discrete domain with the appropriate filter width.

    References
    ----------
    * [1] https://hdl.handle.net/10012/20779

    """
    # start with large kernel size and truncate down until satisfied
    N = 501

    grid_x, grid_y = make_grid(N = N)
    shapelet = orthonormalpolar2D_n1(m=m, x1=grid_x, x2=grid_y, beta=beta)

    accept = False

    while not accept:
        edgeweight = np.abs(np.real(shapelet[int(shapelet.shape[0]/2), -1])) / np.real(shapelet).max()

        if edgeweight < 0.001:
            N -= 4
            grid_x, grid_y = make_grid(N = N)
            shapelet = orthonormalpolar2D_n1(m=m, x1=grid_x, x2=grid_y, beta=beta)
        else:
            accept = True

    return shapelet