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

from typing import Union
import warnings

import numpy as np
from scipy.signal import fftconvolve

from .kernel import get_opt_kernel_n0, get_opt_kernel_n1
from .scaling import lambda_to_beta_n0, lambda_to_beta_n1
from .wavelength import get_wavelength

__all__ = [
    'convresponse_n0',
    'convresponse_n1',
]


def convresponse_n0(image: np.ndarray, shapelet_order: Union[str,int] = 'default', verbose: bool = True):
    r""" 
    This function computes the convolution between a range of shapelets kernels and an image, extracting the magnitude of response as well as the shapelet-based orientation as per the steerable shapelet formulism[RS_convresponse_n0]_.
    
    Parameters
    ----------
    * image: np.ndarray
        * The image to be convolved with shapelet kernels
    * shapelet_order: Union[str,int]
        * Set as 'default' to use higher-order shapelets[MT_convresponse_n0]_ ($m \leq m'$). Can also accept integer value such that analysis uses $m \in [1, shapelet_{order}]$
    * verbose: bool, optional
        * True (default) to print out information from convolution operation to console

    Returns
    -------
    * omega: numpy.ndarray
        * The magnitude of (maximum) convolutional response as a 3D array as per steerable shapelet formulism
    * phi: numpy.ndarray
        * The shapelet orientation at maximum response normalized to $[0, 2pi/m)$

    Notes
    -----
    This function uses the orthonormal polar shapelet definition for $n=0$ shapelets[TA_convresponse_n0]_ (see shapelets.functions.orthonormalpolar2D_n0).

    References
    ----------
    .. [RS_convresponse_n0] http://dx.doi.org/10.1103/PhysRevE.91.033307
    .. [MT_convresponse_n0] http://dx.doi.org/10.1088/1361-6528/ad1df4
    .. [TA_convresponse_n0] https://doi.org/10.1088/1361-6528/aaf353

    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image parameter must be a numpy array.')

    if isinstance(shapelet_order, str):
        if shapelet_order == 'default': 
            mmax = None
        else:
            raise ValueError('shapelet_order parameter as a str must be "default".')
    elif isinstance(shapelet_order, int):
        mmax = shapelet_order
    else:
        raise TypeError('shapelet_order parameter must either be "default" or integer value.')

    # get characteristic wavelength of image 
    l = get_wavelength(image=image, verbose=verbose)

    minRespTol = 0.1
    
    Ny, Nx = image.shape
    omegaTotal = []

    # predefined maximum m value (mmax)
    if mmax != None:
        omega = np.empty((Ny, Nx, mmax)) 
        phi = np.empty((Ny, Nx, mmax))
        for i in range(mmax):
            # get beta
            beta = lambda_to_beta_n0(m=i+1, l=l)

            # get grid for discretization and initialize shapelet kernel
            shapelet = get_opt_kernel_n0(m=i+1, beta=beta)

            # convolve kernel (shapelet) with image
            con = fftconvolve(image, shapelet, mode = 'same')
            omega[:,:,i] = np.abs(con)
            phi[:,:,i] = np.angle(con)

        if verbose:
            print(f"Convolution complete for shapelets m <= {mmax}")

    # use iteration scheme from ref.[MT]_ to get maximum shapelet order
    else:
        omega = np.empty((Ny, Nx, 200)) 
        phi = np.empty((Ny, Nx, 200))
        currResp = 1.
        m = 0
        while currResp > minRespTol:
            # get beta
            m += 1
            beta = lambda_to_beta_n0(m=m, l=l)

            # get grid for discretization and initialize shapelet kernel
            shapelet = get_opt_kernel_n0(m=m, beta=beta)
            
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

    # to correct angles on [0, 2pi/m] as per steerable shapelet theory from ref [RS]_.
    for i in range(phi.shape[2]):
        phi[:,:,i] = (phi[:,:,i] - phi[:,:,i].min()) / (phi[:,:,i].max() - phi[:,:,i].min())
        phi[:,:,i] *=  2*np.pi / (i+1)

    return omega, phi

def convresponse_n1(image: np.ndarray, mmax: int, verbose=True):
    r""" 
    This function computes the convolution between a range of shapelets kernels and an image, extracting the magnitude of response as well as the shapelet-based orientation as per the steerable shapelet formulism[RS_convresponse_n1]_.
    
    Parameters
    ----------
    * image: np.ndarray
        * The image to be convolved with shapelet kernels
    * mmax: int
        * Maximum $m$ shapelet parameter to compute convolutions. Note that $m \geq 0$
    * verbose: bool, optional
        * True (default) to print out information from convolution operation to console

    Returns
    -------
    * omega: numpy.ndarray
        * The magnitude of (maximum) convolutional response as a 3D array
    * phi: numpy.ndarray
        * The shapelet orientation at maximum response normalized to $[0, 2pi/m)$

    Notes
    -----
    This function uses the orthonormal polar shapelet definition for $n=1$ shapelets[MT_convresponse_n1]_ (see shapelets.functions.orthonormalpolar2D_n1).

    References
    ----------
    .. [RS_convresponse_n1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    .. [MT_convresponse_n1] https://hdl.handle.net/10012/20779

    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image parameter must be a numpy array.')
    
    if not isinstance(mmax, int):
        raise TypeError('mmax parameter must be of type int.')
    elif mmax >= 10:
        msg = "WARNING: Desired shapelet behaviour is declining as m increases beyond 10. See Section 6.3 from https://hdl.handle.net/10012/20779 for more details."
        warnings.warn(msg)

    # get characteristic wavelength of image 
    l = get_wavelength(image=image, verbose=verbose)

    Ny, Nx = image.shape

    omega = np.empty((Ny, Nx, mmax)) 
    phi = np.empty((Ny, Nx, mmax))

    for i in range(mmax):
        # get optimal beta from numerical scheme
        beta = lambda_to_beta_n1(m=i+1, l=l)

        # get optimal kernel size
        shapelet = get_opt_kernel_n1(m = i+1, beta = beta)

        # convolve kernel (shapelet) with image
        con = fftconvolve(image, shapelet, mode = 'same')
        omega[:,:,i] = np.abs(con)
        phi[:,:,i] = np.angle(con)
    
    if verbose:
        print(f"Convolution complete for shapelets m <= {mmax}")
            
    # normalize response vectors
    norms = np.linalg.norm(omega, axis = 2)
    omega = omega / norms.reshape(Ny, Nx, 1)

    # to correct angles on [0, 2pi/m] as per steerable shapelet theory from ref [RS]_.
    for i in range(phi.shape[2]):
        phi[:,:,i] = (phi[:,:,i] - phi[:,:,i].min()) / (phi[:,:,i].max() - phi[:,:,i].min())
        phi[:,:,i] *=  2*np.pi / (i+1)

    return omega, phi