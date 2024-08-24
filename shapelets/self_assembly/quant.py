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

import ctypes
from pathlib import Path
import os
import platform
import time 
from typing import Union

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq
from scipy.signal import fftconvolve
from scipy.ndimage import grey_dilation, median_filter
 
from .convolution import convresponse_n0
from .kernel import get_opt_kernel_n0
from .misc import trim_image
from .scaling import lambda_to_beta_n0
from .wavelength import get_wavelength

__all__ = [
    'defectid',
    'orientation',
    'rdistance',
]


def defectid(image: np.ndarray, pattern_order: str, verbose: bool = True):
    r""" 
    Computes the defect identification method from ref. [1]. Also known as the defect response distance method in ref. [1].

    Parameters
    ----------
    * image: numpy.ndarray
        * The image loaded as a numpy array
    * pattern_order: str
        * Pattern order (symmetry type). Options are: 'stripe', 'square', 'hexagonal'
    * verbose: bool, optional
        * True (default) to print out information from convolution operation to console
    
    Returns
    -------
    * centroids: np.ndarray
        * The centroids from k-means clustering [2]. Each centroid is a row vector
    * clusterMembers2D: np.ndarray
        * Shows which cluster each pixel from image is a member of. I.e., value of x would mean it belongs to the cluster who's centroid is defined by centroids[x] (in numpy array notation)
    * defects: np.ndarray
        * The result of the defect response distance method [1]

    References
    ----------
    * [1] http://dx.doi.org/10.1088/1361-6528/ad1df4
    * [2] https://doi.org/10.1007/978-3-642-29807-3

    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image must be a numpy array.')

    if not isinstance(pattern_order, str):
        raise TypeError('pattern_order parameter must be of str type.')
    elif pattern_order not in ['stripe', 'square', 'hexagonal']:
        raise ValueError('pattern_order parameter only accepts "stripe", "square", "hexagonal" str values.')
    
    # enforce appropriate number of clusters depending on pattern_order
    min_clusters = {'stripe': 4, 'square': 8, 'hexagonal': 10}
    num_clusters = min_clusters[pattern_order]
    
    # get convolutional response data 
    response = convresponse_n0(image = image, shapelet_order = 'default', verbose=verbose)[0]
    response2D = response.reshape(-1, response.shape[-1])
    
    # clustering 
    t1 = time.time()
    if verbose:
        print(f"Performing k-means clustering with k={num_clusters}, this may take a while...")
    centroids = kmeans(response2D, num_clusters)[0]
    clusterMembers1D, dists1D = vq(response2D, centroids)
    clusterMembers2D = clusterMembers1D.reshape(response.shape[0:2]) 
    
    t2 = time.time() - t1
    if verbose:
        print(f"Clustering runtime = {t2:0.3} s")

    # get inputs of selected clusters
    plt.imshow(clusterMembers2D, cmap='jet')
    plt.axis('off')
    plt.title('a = add point; del/backspace = remove point; enter = finish')
    win_positions = np.array(plt.ginput(n = -1, timeout = -1, mouse_add=None, mouse_pop=None, mouse_stop=None))
    win_positions = np.round(win_positions, 0).astype(int)

    # now mask out non-selected clusters
    dists1D = (dists1D - dists1D.min()) / (dists1D.max() - dists1D.min())
    dists2D = dists1D.reshape(response.shape[0:2])
    defects = np.zeros((response.shape[0], response.shape[1]))

    selected_clusters = []
    for i in range(win_positions.shape[0]):
        x, y = win_positions[i][0], win_positions[i][1]
        cluster = clusterMembers2D[y, x] 

        if cluster not in selected_clusters:
            selected_clusters.append(cluster)
            # mask out the cluster from non-trimmed data, clusterMembers2D
            defects += np.where(clusterMembers2D == int(cluster), 1, 0)
    
    # compute defect response distance
    defects = defects * dists2D
    
    return centroids, clusterMembers2D, defects 

def orientation(image: np.ndarray, pattern_order: str, verbose: bool = True):
    r""" 
    Computes the local pattern orientation from ref. [1] via an iterative scheme using shapelet orientation at maximum response from steerable filter theory [2].

    Parameters
    ----------
    * image: numpy.ndarray
        * The image loaded as a numpy array
    * pattern_order: str
        * Pattern order (symmetry type). Options are: 'stripe', 'square', 'hexagonal'
    * verbose: bool, optional
        * True (default) to print out results of orientation algorithm to console

    Returns
    -------
    * mask: np.ndarray
        * The mask for well-defined features
    * dilate: np.ndarray
        * The dilated mask
    * orientation: np.ndarray
        * Applying smoothing/blending to the dilated mask via median filter kernel [3]
    * maxval: float
        * The maximum allowed orientation value, where $maxval = \frac{2 \pi}{m}$
    
    Notes
    -----
    This function uses shapelets.self_assembly.misc.trim_image during iteration to converge on an acceptable orientation result. Therefore, the orientation result will **not** have the same shape as the original image.

    References
    ----------
    * [1] http://dx.doi.org/10.1088/1361-6528/ad1df4
    * [2] https://doi.org/10.1109/34.93808
    * [3] https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.median_filter.html
    
    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image must be a numpy array.')
    
    if not isinstance(pattern_order, str):
        raise TypeError('pattern_order parameter must be of str type.')
    elif pattern_order not in ['stripe', 'square', 'hexagonal']:
        raise ValueError('pattern_order parameter only accepts "stripe", "square", "hexagonal" str values.')

    # get orientation information based on pattern_order
    params = {'stripe': 0, 'square': 3, 'hexagonal': 5}
    ind = params[pattern_order]
    maxval = 2*np.pi / (ind+1)
    
    # get characteristic wavelength of image 
    l = get_wavelength(image=image, verbose=False)

    # get convolutional response data up to m=6 (higher-order shapelets not needed for this method)
    # note that custom convolutional response function embedded here since vectors need to be independently normalized

    Ny, Nx = image.shape
    mmax = 6

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
    
    # normalize response individually, not in terms of vectors across m values
    for i in range(omega.shape[2]):
            omega[:,:,i] =  (omega[:,:,i] - omega[:,:,i].min()) / ( omega[:,:,i].max() - omega[:,:,i].min())

    # to correct angles on [0, 2pi/m] as per steerable shapelet theory.
    for i in range(phi.shape[2]):
        phi[:,:,i] = (phi[:,:,i] - phi[:,:,i].min()) / (phi[:,:,i].max() - phi[:,:,i].min())
        phi[:,:,i] *=  2*np.pi / (i+1)

    # find the response threshold iteratively 
    orient = phi[:,:,ind].copy()
    resp_og = omega[:,:,ind].copy()
    dilationsize = int( np.round(2*l, 0) )
    blendsize = int( np.round(4*l, 0) )
    
    accept_solution = False
    resptol = 1.0
    errtol = 0.01
    
    if verbose:
        print(f"Beginning iteration with response tolerance = {errtol}\n")

    while not accept_solution:
        resp = np.where(resp_og > resptol, 1, 0)
        mask = trim_image((orient * resp), l)
        
        dilate = grey_dilation(mask, size=dilationsize)
        orientation_final = median_filter(dilate, size=blendsize)
    
        # compute error on undefined values after blending
        err = (orientation_final == 0.0).sum() / orientation_final.size
            
        if err > errtol:
            # TODO: Adaptive step width for resptol to decrease runtime
            resptol -= 0.01
            resptol = np.round(resptol, 2)
            if verbose:
                print(f"Orientation failed with error {err:0.5}. Reducing threshold to {resptol}")
        elif resptol < 0:
            raise RuntimeError('Orientation failed to produce plot.')
        else:
            if verbose:
                print(f"Orientation successful with error {err:0.5}")
            accept_solution = True  

    return mask, dilate, orientation_final, maxval

def rdistance(image: np.ndarray, num_clusters: Union[str,int] = 'default', shapelet_order: Union[str,int] = 'default', ux: Union[str,list] = 'default', uy: Union[str,list] = 'default', verbose: bool = True) -> np.ndarray:
    r""" 
    Compute the response distance method from ref. [1]. By default, attempts to use the fastest implementation (C++) as opposed to Python; defaults to Python upon error. 

    Parameters
    ----------
    * image: numpy.ndarray
        * The image loaded as a numpy array
    * num_clusters: Union[str,int]
        * The number of clusters as input to k-means clustering [2]. If str, acceptable value is "default" (which uses 20 clusters [3])
    * shapelet_order: Union[str,int]
        * Set as 'default' to use higher-order shapelets [4] ($m \leq m'$). Can also accept integer value such that analysis uses $m \in [1, shapelet_{order}]$
    * ux: Union[str,list]
        * The bounds in the x-direction for the reference region. If using list option, must be 2 element list. Choosing "default" will force user to choose ref. region during runtime
    * uy: Union[str,list]
        * The bounds in the y-direction for the reference region. If using list option, must be 2 element list. Choosing "default" will force user to choose ref. region during runtime
    * verbose: bool, optional
        True (default) to print out results of response distance method to console

    Returns
    -------
    * d: np.ndarray
        * The response distance scalar field. Its dimensions are the same as the input image

    References
    ----------
    * [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    * [3] https://doi.org/10.1088/1361-6528/aaf353
    * [2] https://doi.org/10.1007/978-3-642-29807-3
    * [4] http://dx.doi.org/10.1088/1361-6528/ad1df4

    """
    if not isinstance(image, np.ndarray):
        raise TypeError('image must be a numpy array.')
        
    if isinstance(num_clusters, str):
        if num_clusters == 'default': 
            num_clusters = 20
        else:
            raise ValueError('If num_clusters is str type, must be "default" otherwise use int.')
    elif not isinstance(num_clusters, int):
        raise TypeError('If num_clusters is not str type, must be int.')

    if type(ux) != type(uy):
        raise TypeError('ux and uy parameters must be both be "default" or both 2-element lists.')
    
    elif isinstance(ux, str):
        if ux == 'default' and uy == 'default':
            choose_ref = True 
        else:
            raise ValueError('As str types, ux and uy parameters must be "default".')
    
    elif isinstance(ux, list):
        if len(ux) != 2 or len(uy) != 2:
            raise ValueError('ux or uy has less or more than 2 elements.')
        else:
            ux = [int(val) for val in ux]
            uy = [int(val) for val in uy]
            choose_ref = False
    
    if choose_ref:
        num_bounds = 0
        print("Please select 4 corner points: a = add point; del/backspace = remove point; enter = finish")
        while num_bounds != 4:
            # Show the image to user, let them select ref zone
            plt.figure(1, figsize=(12,12))
            plt.imshow(image, cmap = 'gray')
            plt.axis('off')
            #plt.get_current_fig_manager().full_screen_toggle()
            plt.title('a = add point; del/backspace = remove point; enter = finish')
            win_positions = np.array(plt.ginput(n = -1, timeout = -1, mouse_add=None, mouse_pop=None, mouse_stop=None))

            # check
            if win_positions.shape[0] == 4:
                ux = [ int(win_positions[:,0].min()), int(win_positions[:,0].max()) ] 
                uy = [ int(win_positions[:,1].min()), int(win_positions[:,1].max()) ]
                num_bounds = 4
                print("User-defined subdomain successfully chosen")
            else:
                print("Failed to choose four (4) corner points, please try again")

            plt.close()
    
        # now display user chosen rectangle and image
        """win = np.zeros_like(image)
        X, Y = np.meshgrid(np.arange(ux[0], ux[1]), np.arange(uy[0], uy[1]))
        win[Y, X] = 1
        plt.figure(1, figsize=(7,7))
        plt.imshow(image, cmap = 'gray')
        plt.imshow(win, cmap = 'jet', alpha = 0.5)
        plt.title('Image with reference region', fontsize = 12)
        plt.axis('off')
        plt.show()"""
    
    # get convolutional response data, enforce shapelet_order parameter in convresponse() function
    response = convresponse_n0(image = image, shapelet_order = shapelet_order, verbose=verbose)[0]

    # compute response distance
    Ny, Nx = response.shape[0], response.shape[1]
    uX, uY = np.meshgrid(np.arange(ux[0], ux[1] + 1), np.arange(uy[0], uy[1] + 1))
    response_ref_whole = response[uY, uX] 
    response_ref_whole = response_ref_whole.reshape( -1, response_ref_whole.shape[-1] )

    if num_clusters != 0:
        response_ref, distortion = kmeans(response_ref_whole, num_clusters)
        if verbose:
            print(f"kmeans successful with {num_clusters} centroids & distortion value of: {distortion:0.3}")
    else:
        response_ref = response_ref_whole.copy()
        if verbose:
            print("Proceeding to compute response distance without k-means clustering:")

    # prioritize C++ implementation, any errors should resort to python implementation
    ti = time.time()

    try:
        print("Attempting to use C++ implementation of response distance")
        response_2d = np.reshape(response, (-1, response.shape[-1]))
        d_1d = _rdistance(response_ref, response_2d)
        d = d_1d.reshape(Ny, Nx)
    
    except Exception as err:
        print(f"C++ implementation failed: {repr(err)}.\nResorting to Python implementation\n")

        d = np.zeros((Ny, Nx))
        compList = np.array([10, 25, 50, 75, 100]).astype(int)

        for i in range(Nx):
            if int(100* i / Nx) in compList:
                compList = compList[1:]
                if verbose:
                    print(f"Response distance {int(100* i / Nx)}% complete")
            for j in range(Ny):
                dists = np.zeros(response_ref.shape[0])
                for refvec in range(response_ref.shape[0]):
                    dists[refvec] = np.linalg.norm(response[j, i] - response_ref[refvec])
                d[j, i] = dists.min()
            
    tf = time.time()

    if verbose:
        print(f"Response distance complete with runtime of {tf-ti:0.2}s")

    return d

def _rdistance(refVectors: np.ndarray, testVectors: np.ndarray) -> np.ndarray:
    r"""
    Wrapper function for C++ implementation of response distance method [a]. Heavily reliant on ctypes library. On average, this C++ implementation is 14-16x faster than Python [b].

    Parameters
    ----------
    * refVectors : np.ndarray
        * The reference response vectors as a 2-dimensional array
    * testVectors : np.ndarray
        * The test (or non-reference) response vectors as a 2-dimensional array

    Returns
    -------
    * rdists: np.ndarray
        * The response distances as a 1-dimensional array (must be reshaped to match image dimensions)

    Notes
    -----
    Any changes made to _rdistance.cpp requires re-compiling the shared library via g++ -fPIC -shared -o _rdistance.so _rdistance.cpp

    References
    ----------
    * [a] http://dx.doi.org/10.1103/PhysRevE.91.033307
    * [b] https://hdl.handle.net/10012/20779

    """
    # ensure input vectors are of type numpy.float64
    refVectors = refVectors.astype(np.float64)
    testVectors = testVectors.astype(np.float64)

    # grab lists of synomyms for architecture CPU names
    archx86 = ['x86_64', 'x86', 'amd64']
    archarm = ['aarch64', 'arm64', 'armv8', 'armv9']

    # grab operating system and cpu arch info
    ostype = platform.system()
    arch   = platform.machine().lower()

    if 'Windows' == ostype:
        if arch not in archx86:
            raise NotImplementedError('Only AMD64 windows is supported.')
        else:
            # grab relative path of shared library file for windows
            cpath = os.path.join(Path(__file__).parents[0], '_rdistance_win_amd64.so')

            # load shared windows library
            cpplib = ctypes.CDLL(cpath, winmode=0)

    elif 'Linux' == ostype:
        if arch not in archx86:
            raise NotImplementedError('Only AMD64 linux is supported.')
        else:
            # grab relative path of shared library file for linux
            cpath = os.path.join(Path(__file__).parents[0], '_rdistance_nix_amd64.so')

            # load shared linux library
            cpplib = ctypes.CDLL(cpath)
            
    elif 'Darwin' == ostype:
        if arch not in archarm:
            raise NotImplementedError('Only ARM64 macOS is supported.')
        else:
            # grab relative path of shared library file for linux
            cpath = os.path.join(Path(__file__).parents[0], '_rdistance_mac_arm64.so')

            # load shared mac library
            cpplib = ctypes.CDLL(cpath)

    else:
        raise NotImplementedError('Only Windows, Linux, and macOS are supported.')

    # setup argument and return types
    cpplib.rdistance.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS'), 
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS'),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int]

    cpplib.rdistance.restype = ctypes.POINTER(ctypes.c_double)

    # prepare arguments. reinforce int to coincide with c++ function inputs
    numrefs = int(refVectors.shape[0])
    numtest = int(testVectors.shape[0])
    mmax = int(testVectors.shape[1])

    ptrRdistance = cpplib.rdistance(refVectors, testVectors, numrefs, numtest, mmax)

    # access entire memory space from pointer
    rdists = np.ctypeslib.as_array(ptrRdistance, shape=(numtest,))

    return rdists
