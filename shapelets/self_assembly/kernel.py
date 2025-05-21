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
This module holds functions related to kernels, including convolutions between shapelet filters and images.
"""


from typing import Union
import warnings

import numpy as np
from scipy.signal import fftconvolve

from shapelets.functions import(
    orthonormalpolar2D_n0, 
    orthonormalpolar2D_n1
)
import shapelets.self_assembly.wavelength as wavelength


def convresponse_n0(
    image: np.ndarray, 
    shapelet_order: Union[str,int] = 'default', 
    verbose: bool = True
):
    r""" This function computes the convolution between a range of shapelets kernels 
    and an image, extracting the magnitude of response as well as the 
    shapelet-based orientation as per the steerable shapelet formulism [1]_.
    
    Parameters
    ----------
    image : np.ndarray
        The image to be convolved with shapelet kernels
    shapelet_order : Union[str,int]
        Set as 'default' to use higher-order shapelets [1]_ (:math:`m \leq m'`). 
        Can also pass integer value for filter m upper bound but value must be > 0
    verbose : bool, optional
        True (default) to print out information from convolution operation to console

    Returns
    -------
    omega : numpy.ndarray
        The magnitude of (maximum) convolutional response as a 3D array as 
        per steerable shapelet formulism
    phi : numpy.ndarray
        The shapelet filter optimal orientation (corresponding to maximum convolutional response) 
        for the steerable shapelet formulism

    Notes
    -----
    This function uses the orthonormal polar shapelet definition for 
    :math:`n=0` shapelets [2]_ (see shapelets.functions.orthonormalpolar2D_n0).

    References
    ----------
    .. [1] https://hdl.handle.net/10012/20779
    .. [2] http://dx.doi.org/10.1088/1361-6528/ad1df4
    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image parameter must be a numpy array.')

    if isinstance(shapelet_order, str):
        if shapelet_order == 'default': 
            mmax = None
        else:
            raise ValueError('mmax parameter as a str must be "default".')
    elif not isinstance(shapelet_order, int):
        raise TypeError('mmax parameter must either be "default" or integer value.')
    elif shapelet_order <=0:
        raise ValueError('mmax parameter, if passed as an integer, must be > 0.')
    else:
        mmax = shapelet_order

    # get characteristic wavelength of image 
    l = wavelength.get_wavelength(image=image, verbose=verbose)

    minRespTol = 0.1
    
    Ny, Nx = image.shape
    omegaTotal = []

    # predefined maximum m value (mmax)
    if mmax != None:
        omega = np.empty((Ny, Nx, mmax)) 
        phi = np.empty((Ny, Nx, mmax))
        for i in range(mmax):
            # get beta
            beta = wavelength.lambda_to_beta_n0(m=i+1, l=l)

            # get grid for discretization and initialize shapelet kernel
            shapelet = get_optimal_kernel_n0(m=i+1, beta=beta)

            # convolve kernel (shapelet) with image
            con = fftconvolve(image, shapelet, mode = 'same')
            omega[:,:,i] = np.abs(con)
            phi[:,:,i] = np.angle(con)

        if verbose:
            print(f"Convolution complete for shapelets m <= {mmax}")

    # use iteration scheme from ref. [2] to get maximum shapelet order
    else:
        omega = np.empty((Ny, Nx, 200)) 
        phi = np.empty((Ny, Nx, 200))
        currResp = 1.
        m = 0
        while currResp > minRespTol:
            # get beta
            m += 1
            beta = wavelength.lambda_to_beta_n0(m=m, l=l)

            # get grid for discretization and initialize shapelet kernel
            shapelet = get_optimal_kernel_n0(m=m, beta=beta)
            
            con = fftconvolve(image, shapelet, mode = 'same')
            omegacurr = np.abs(con)

            omegaTotal.append(np.sum(omegacurr))
            currResp = np.sum(omegacurr) / np.max(omegaTotal)
            
            omega[:,:,m-1] = np.abs(con)
            phi[:,:,m-1] = np.angle(con)
            
        # remove last convolutional data since it broke the while loop, true m = m -1
        m -= 1
        omega = omega[:,:,:m]
        phi = phi[:,:,:m]
        if verbose:
            print(f"Convolution complete for shapelets m <= {m} before tolerance exceeded")

    # normalize response vectors
    norms = np.linalg.norm(omega, axis = 2)
    omega = omega / norms.reshape(Ny, Nx, 1)

    # to compute optimal filter orientations as per the steerable shapelet formulism
    for i in range(phi.shape[2]):
        phi[:,:,i] /=  i+1

    return omega, phi


def convresponse_n1(
    image: np.ndarray, 
    mmax: int, 
    verbose=True
):
    r""" This function computes the convolution between a range of shapelets kernels 
    and an image, extracting the magnitude of response as well as the 
    shapelet-based orientation as per the steerable shapelet formulism in [1]_.
    
    Parameters
    ----------
    image : np.ndarray
        The image to be convolved with shapelet kernels
    mmax : int
        Maximum :math:`m` shapelet parameter to compute convolutions. 
        Note that :math:`m \geq 0`
    verbose : bool, optional
        True (default) to print out information from convolution operation to console

    Returns
    -------
    omega : numpy.ndarray
        The magnitude of (maximum) convolutional response as a 3D array
    phi : numpy.ndarray
        The shapelet filter optimal orientation (corresponding to maximum convolutional response) 
        for the steerable shapelet formulism

    Notes
    -----
    This function uses the orthonormal polar shapelet definition 
    for :math:`n=1` shapelets [1]_ (see also shapelets.functions.orthonormalpolar2D_n1).

    References
    ----------
    .. [1] https://hdl.handle.net/10012/20779
    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image parameter must be a numpy array.')
    
    if not isinstance(mmax, int):
        raise TypeError('mmax parameter must be of type int.')
    elif mmax >= 10:
        msg = "WARNING: Desired shapelet behaviour is declining as m increases beyond 10. See Section 6.3 from https://hdl.handle.net/10012/20779 for more details."
        warnings.warn(msg)
    elif mmax < 0:
        raise ValueError('mmax parameter must be >= 0.')

    # get characteristic wavelength of image 
    l = wavelength.get_wavelength(image=image, verbose=verbose)

    Ny, Nx = image.shape

    omega = np.empty((Ny, Nx, mmax)) 
    phi = np.empty((Ny, Nx, mmax))

    for i in range(mmax):
        # get optimal beta from numerical scheme
        beta = wavelength.lambda_to_beta_n1(m=i+1, l=l)

        # get optimal kernel size
        shapelet = get_optimal_kernel_n1(m = i+1, beta = beta)

        # convolve kernel (shapelet) with image
        con = fftconvolve(image, shapelet, mode = 'same')
        omega[:,:,i] = np.abs(con)
        phi[:,:,i] = np.angle(con)
    
    if verbose:
        print(f"Convolution complete for shapelets m <= {mmax}")
            
    # normalize response vectors
    norms = np.linalg.norm(omega, axis = 2)
    omega = omega / norms.reshape(Ny, Nx, 1)

    # to compute optimal filter orientations as per the steerable shapelet formulism
    for i in range(phi.shape[2]):
        phi[:,:,i] /=  i+1

    return omega, phi


def make_grid(N: int):
    r""" Make discretized grid based on width (N).
    
    Parameters
    ----------
    N : int
        The width of the kernel (odd numbers only)

    Returns
    -------
    grid_x : np.ndarray
        The grid's x coordinate space
    grid_y : np.ndarray
        The grid's y coordinate space
    
    Notes
    -----
    As per convention, N should only be an odd number. 
    Additionally, note that grid_x = grid_y.

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


def get_optimal_kernel_n0(
    m: int, 
    beta: float
):
    r""" Determines the optimal filter (kernel) width for an :math:`n=0` orthonormal polar
    shapelet function [1]_ based on :math:`\beta`, the shapelet length-scale parameter.
    
    Parameters
    ----------
    m : int
        Shapelet degree of rotational symmetry
    beta : float
        The characteristic shapelet length scale parameter
    
    Returns
    -------
    shapelet : np.ndarray
        Shapelet function casted onto a discrete domain with the appropriate filter width

    References
    ----------
    .. [1] https://doi.org/10.1088/1361-6528/aaf353
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


def get_optimal_kernel_n1(
    m: int, 
    beta: float
):
    r""" 
    Determines the optimal filter (kernel) width for an :math:`n=1` orthonormal polar
    shapelet function [1]_ based on :math:`\beta`, the shapelet length-scale parameter.

    Parameters
    ----------
    m : int
        Shapelet degree of rotational symmetry
    beta : float
        The characteristic shapelet length scale parameter.
    
    Returns
    -------
    shapelet : np.ndarray
        Shapelet function casted onto a discrete domain with the appropriate filter width.

    References
    ----------
    .. [1] https://hdl.handle.net/10012/20779
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