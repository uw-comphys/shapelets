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

from math import comb as choose

import numpy as np
from scipy.special import binom, erf

from ..functions import cartesian1D, cartesian2D

SQRTPI = np.sqrt(np.pi)

def decompose_analytic(image: np.ndarray, n_max: int, beta: float, centroid: np.ndarray, nspace: list[tuple[int, int]]=None) -> np.ndarray:
    r"""
    Decomposes image into shapelet coefficents analytically by evaluating a series of integrals.

    Parameters
    ----------
    * image: np.ndarray
        * data to be decomposed into shapelet functions
    * n_max: int
        * maximum order of shapelets
    * beta: float
        * characteristic shapelet scale that the object was decomposed at
    * centroid: np.ndarray (dtype=float)
        * center of shapelet reconstruction (relative to image dimensions)
    * nspace: [(int, int)], optional
        * list of shapelet coefficients to be used in the reconstruction. Default is None

    Returns
    -------
    * coefficients: np.ndarray (dtype=float)
        * matrix of shapelet coefficients representing the decomposition of the image
    
    Notes
    -----
    Expands f into smallest square matrix that can contain f.

    """
    if nspace == None:
        nspace = get_nspace(n_max)

    coefficients = np.zeros([n_max+1]*2)
    i = max(image.shape)
    [x, y] = np.arange(0, i) - centroid.reshape(-1,1)

    Ix = np.zeros([n_max+1, i])
    Ix[0, :] = np.sqrt(beta*SQRTPI/2) * (erf( (x.T+1)/(np.sqrt(2)*beta) ) - erf( x.T/(np.sqrt(2)*beta) ))
    Ix[1, :] = -beta*np.sqrt(2) * (cartesian1D(0, x+1, beta)  - cartesian1D(0, x, beta))
    for n in range(2, n_max+1):
        Ix[n, :] = -beta*np.sqrt(2/n) * (cartesian1D(n-1, x+1, beta) - cartesian1D(n-1, x, beta)) + np.sqrt(1-1/n)*Ix[n-2, :]

    Iy = np.zeros([n_max+1, i])
    Iy[0, :] = np.sqrt(beta*SQRTPI/2) * (erf( (y.T+1)/(np.sqrt(2)*beta) ) - erf( y.T/(np.sqrt(2)*beta) ))
    Iy[1, :] = -beta*np.sqrt(2) * (cartesian1D(0, y+1, beta) - cartesian1D(0, y, beta))
    for n in range(2, n_max+1):
        Iy[n, :] = -beta*np.sqrt(2/n) * (cartesian1D(n-1, y+1, beta) - cartesian1D(n-1, y, beta)) + np.sqrt(1-1/n)*Iy[n-2, :]

    for n in nspace:
        j = np.nditer(image, flags=['multi_index'])
        while not j.finished:
            coefficients[n] += image[j.multi_index] * Ix[n[0], j.multi_index[0]] * Iy[n[1], j.multi_index[1]]
            j.iternext()  

    return coefficients

def decompose_kernel(image: np.ndarray, n_max: int, beta: float, centroid: np.ndarray, nspace: list[tuple[int, int]]=None) -> np.ndarray:
    r"""
    Decomposes image into shapelet coefficents using projection of image onto kernels.

    Parameters
    ----------
    * image: np.ndarray
        * data to be decomposed into shapelet functions
    * n_max: int
        * maximum order of shapelets
    * beta: float
        * characteristic shapelet scale that the object was decomposed at
    * centroid: np.ndarray (dtype=float)
        * center of shapelet reconstruction (relative to image dimensions)
    * nspace: [(int, int)], optional
       * list of shapelet coefficients to be used in the reconstruction. Default is None

    Returns
    -------
    * coefficients : np.ndarray (dtype=float)
        * matrix of shapelet coefficients representing the decomposition of the image

    """
    coefficients = np.zeros([n_max+1]*2)
    x = np.arange(0, image.shape[0]) - centroid[0]
    y = np.arange(0, image.shape[1]) - centroid[1]

    x = np.expand_dims(x, axis=1)
    y = np.expand_dims(y, axis=1).T

    if nspace == None:
        nspace = get_nspace(n_max)

    for n in nspace:
        kernel = cartesian2D(n[0], n[1], x, y, beta)
        
        # by defintion, the shapelet kernels should be normalized
        coefficients[n] = np.sum(kernel * image) #/ np.sum(kernel**2)
    
    return coefficients

def reconstruct(s_coeff: np.ndarray, n_max: int, beta: float, centroid: np.ndarray, dimensions: tuple[int, int], nspace: list[tuple]=None) -> np.ndarray:
    r"""
    Given a matrix of shapelet coefficients, constructs image.

    Parameters
    ----------
    * s_coeff: np.ndarray (dtype=float)
        * matrix of shapelet coefficients
    * n_max: int
        maximum order of shapelets
    * beta: float
        * characteristic shapelet scale that the object was decomposed at
    * centroid: np.ndarray (dtype=float)
        * center of shapelet reconstruction (relative to image dimensions)
    * dimensions: (int, int)
        * the resolution of the image
    * nspace: [(int, int)], optional
        * list of shapelet coefficients to be used in the reconstruction. Default is None
    
    Returns
    -------
    * image: np.ndarray (dtype=float)
        * the reconstructed image
    
    """
    if nspace == None:
        nspace = get_nspace(n_max)

    image = np.zeros(dimensions)
    x = np.arange(0, dimensions[0]) - centroid[0]
    y = np.arange(0, dimensions[1]) - centroid[1]

    x = np.expand_dims(x, axis=1)
    y = np.expand_dims(y, axis=1).T

    for n in nspace:
        image += s_coeff[n] * cartesian2D(n[0], n[1], x, y, beta)

    return image

# calculate improved parameters to optimize shapelet coeffcients
def update_shapelet_parameters(coeff: np.ndarray, n_max: int, beta: float, centroid: np.ndarray, nspace: list[tuple]=None) -> tuple[float, np.ndarray]:
    r"""
    Calculates an object's characteristic scale and centroid using its calculated shapelet coefficients. These new parameters can be used to decompose the image again with lower error.

    Parameters
    ----------
    * coeff: np.ndarray
        * data to be decomposed into shapelet functions
    * n_max: int
        * maximum order of shapelets
    * beta: float
        * characteristic shapelet scale that the object was decomposed at
    * centroid: np.ndarray (dtype=float)
        * center of shapelet reconstruction (relative to image dimensions)
    * nspace: [(int, int)] (optional)
        * list of shapelet coefficients to be used in the reconstruction. Default is None
    
    Returns
    -------
    * new_beta: float
        * updated shapelet scale for future decomposition
    * new_centroid: np.ndarray
        * updated image center for future decomposition

    References
    ----------
    .. [1] https://doi.org/10.1046/j.1365-8711.2003.05901.x

    """
    if nspace == None:
        nspace = get_nspace(n_max)

    flux = SQRTPI*beta * np.sum([ coeff[n]*np.sqrt( (2.0**(2-sum(n)))*choose(n[0], n[0]//2)*choose(n[1], n[1]//2) ) for n in nspace if (n[0]%2==0 and n[1]%2==0) ])
    centroid_dx = (SQRTPI*beta**2/flux) * np.sum([ coeff[n]*np.sqrt( (n[0]+1)*2.0**(2-sum(n))*choose(n[0]+1, (n[0]+1)//2)*choose(n[1], n[1]//2) ) for n in nspace if (n[0]%2==1 and n[1]%2==0) ])
    centroid_dy = (SQRTPI*beta**2/flux) * np.sum([ coeff[n]*np.sqrt( (n[1]+1)*2.0**(2-sum(n))*choose(n[0], (n[0])//2)*choose(n[1]+1, (n[1]+1)//2) ) for n in nspace if (n[0]%2==0 and n[1]%2==1) ])
    size = (SQRTPI*beta**3/flux) * np.sum([ coeff[n]*(1+sum(n))*np.sqrt( 2.0**(4-sum(n))*choose(n[0], n[0]//2)*choose(n[1], n[1]//2) ) for n in nspace if (n[0]%2==0 and n[1]%2==0) ])

    new_centroid = centroid + np.array([centroid_dx, centroid_dy])
    new_beta = np.sqrt( abs(size) )/2 

    return new_beta, new_centroid

def get_nspace(n_max: int) -> np.ndarray:
    r"""
    Returns a set of (n1, n2) combinations such that the sum of the elements of n is less than n_max, i.e. $||n||_1 \leq n_max$.

    Parameters
    ----------
    * n_max: int
        * maximum order of shapelet
        
    Returns
    -------
    * nspace: np.ndarray (dtype=tuple)
        * list of valid (n1, n2) combinations such that $n1 + n2 <= n_max$

    """
    nspace = np.ndarray(int(binom(n_max+2, 2)), dtype=tuple)
    
    k = 0
    for i in range(0, n_max+1):
        for j in range(0, n_max-i+1):
            nspace[k] = (i, j)
            k+=1
    
    return nspace

def get_compressed_nspace(s_coeff: np.ndarray, n_compress: int) -> np.ndarray:
    r"""
    Trims shapelet coefficient to include only the n_compress largest coefficients.

    Parameters
    ----------
    * s_coeff: np.ndarray (dtype=float)
        * matrix of coefficient values
    * n_compress: int
        * number of shapelet coefficients to preserve
        
    Returns
    -------
    * nspace: np.ndarray (dtype=tuple)
        * list of tuples of largest valid (n1, n2) combinations

    Notes
    -----
    Often an image can be accurately reconstructed using only several of the shapelet functions with the largest coefficients. Ignoring smaller coefficient functions helps to avoid overfitting to the image noise.

    Examples
    -----
    Prints the 10 largest coefficients found in the decomposition alongside its shapelet order:
    ```
    coefficients = decompose(data, 5, 1, np.array([0, 0]))
    compressed_nspace = get_compressed_nspace(coefficients, 10)
    for n in compressed_nspace:
        print(f"shapelet order {n}: {coefficients[n]}")
    ```

    """
    if n_compress >= binom(s_coeff.shape[0]+2, 2):
        print('compression factor larger than availible coefficients')
        return get_nspace(s_coeff.shape[0])
    
    idx = np.argwhere(abs(s_coeff) >= np.sort(abs(s_coeff), axis=None)[-n_compress])
    nspace = list( zip(idx[:,0], idx[:,1]) )

    return nspace
