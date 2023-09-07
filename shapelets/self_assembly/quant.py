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

import time 

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq
from scipy.signal import fftconvolve
from scipy.ndimage import grey_dilation, median_filter

from .misc import trimage, make_grid
from .wavelength import lambda_to_beta
from ..functions import orthonormalpolar2D

__all__ = [
    'convresponse',
    'defectid',
    'orientation',
    'rdistance'
]

def convresponse(image, l, shapelet_order = 'default', normresponse = 'Vector'):
    r""" This function computes the convolution between a range of 
         shapelets and an image.
    
    Parameters
    ----------
    image : numpy.ndarray
        The image for convolution with shapelet functions.
    l : float
        The characteristic wavelength of the image.
    shapelet_order : str or int
        'default' to use higher-order shapelets (m<=m') as in ref [3].
        Can also accept integer value to use shapelets for m <= int.
    normresponse : str, optional
        Normalize magnitude of response (omega) in terms of response vectors = "Vector". Default. 
        Normalize each m-fold response wrt itself on [0, 1) = "Individual".

    Returns
    -------
    omega : numpy.ndarray
        The magnitude of response.
    phi : numpy.ndarray
        The shapelet orientation at maximum response on [0, 2pi/m).

    Notes
    -----
    This function uses the orthonormal polar shapelet definition from [1].

    References
    ----------
    .. [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    .. [2] https://doi.org/10.1088/1361-6528/aaf353
    .. [3] TODO: REFTINO

    """
    if shapelet_order == 'default': mmax = None
    else: mmax = int(shapelet_order)
    
    minRespTol = 0.1
    
    Ny, Nx = image.shape
    omegaTotal = []

    if mmax != None:
        omega = np.empty((Ny, Nx, mmax)) 
        phi = np.empty((Ny, Nx, mmax))
        for i in range(mmax):
            # get beta
            beta = lambda_to_beta(m=i+1, l=l)

            # get grid for discretization and initialize shapelet kernel
            N = 21 # minimum
            grid_x, grid_y = make_grid(N = N)
            shapelet = orthonormalpolar2D(m=i+1, x1=grid_x, x2=grid_y, beta=beta)

            # optimize shapelet (kernel) size
            accept = False

            while not accept:
                edgeweight = np.abs(np.real(shapelet[int(shapelet.shape[0]/2), -1])) \
                    / np.real(shapelet).max()
                if edgeweight > 0.0001:
                    N += 4
                    grid_x, grid_y = make_grid(N = N)
                    shapelet = orthonormalpolar2D(m=i+1, x1=grid_x, x2=grid_y, beta=beta)
                else:
                    accept = True

            # convolve kernel (shapelet) with image
            con = fftconvolve(image, shapelet, mode = 'same')
            omega[:,:,i] = np.abs(con)
            phi[:,:,i] = np.angle(con)
        print(f"Convolution complete for shapelets m <= {mmax}")

    else:
        omega = np.empty((Ny, Nx, 200)) 
        phi = np.empty((Ny, Nx, 200))
        currResp = 1.
        m = 0
        while currResp > minRespTol:
            # get beta
            m += 1
            beta = lambda_to_beta(m=m, l=l)

            # get grid for discretization and initialize shapelet kernel
            N = 21 # minimum
            grid_x, grid_y = make_grid(N = N)
            shapelet = orthonormalpolar2D(m=m, x1=grid_x, x2=grid_y, beta=beta)

            # optimize shapelet (kernel) size
            accept = False

            while not accept:
                edgeweight = np.abs(np.real(shapelet[int(shapelet.shape[0]/2), -1])) \
                    / np.real(shapelet).max()
                if edgeweight > 0.0001:
                    N += 4
                    grid_x, grid_y = make_grid(N = N)
                    shapelet = orthonormalpolar2D(m=m, x1=grid_x, x2=grid_y, beta=beta)
                else:
                    accept = True
            
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
        print(f"Convolution complete for shapelets m <= {m} before tolerance exceeded")

    if normresponse == 'Vector': 
        norms = np.linalg.norm(omega, axis = 2)
        omega = omega / norms.reshape(Ny, Nx, 1)
        
    elif normresponse == 'Individual':
        for i in range(omega.shape[2]):
            omega[:,:,i] =  (omega[:,:,i] - omega[:,:,i].min()) / ( omega[:,:,i].max() - omega[:,:,i].min())

    # to correct angles on [0, 2pi/m] as per steerable shapelet theory from ref [1].
    for i in range(phi.shape[2]):
        phi[:,:,i] = (phi[:,:,i] - phi[:,:,i].min()) / (phi[:,:,i].max() - phi[:,:,i].min())
        phi[:,:,i] *=  2*np.pi / (i+1)

    return omega, phi


def defectid(response, l, pattern_order, num_clusters):
    r""" Defect identification method from [1].

    Parameters
    ----------
    response : np.ndarray
        The 3D array corresponding to the response of the convolution for a 
        range of shapelets, obtained from shapelet_response().
    l : float
        The characteristic wavelength of the image.
    pattern_order : str
        Pattern order. Options are: 'stripe', 'square', 'hexagonal'.
    num_clusters : int
        The number of clusters as input to k-means clustering [4].
    
    Returns
    -------
    centroids : np.ndarray
        The centroids from k-means clustering [2].
        Each centroid is a row vector.
    clusterMembers2D : np.ndarray
        Shows which cluster each pixel from image is a member of.
        I.e., value of 1 would mean it belongs to the cluster with centroid as centroids[1].
    defects : np.ndarray
        The result of the defect response distance method. See [1]. 

    Notes
    -----

    References
    ----------
    .. [1] TODO: REFTINO
    .. [2] https://doi.org/10.1007/978-3-642-29807-3


    Examples
    --------

    """
    if pattern_order == 'stripe': 
        if num_clusters == 'default':
            num_clusters = 4
        elif int(num_clusters) < 4:
            print("'num_clusters' parameter too low, defaulting to 4.")
            num_clusters = 4
        else:
            num_clusters = int(num_clusters)
            
    elif pattern_order == 'square': 
        if num_clusters == 'default':
            num_clusters = 8
        elif int(num_clusters) < 8:
            print("'num_clusters' parameter too low, defaulting to 8.")
            num_clusters = 8
        else:
            num_clusters = int(num_clusters)
            
    elif pattern_order == 'hexagonal': 
        if num_clusters == 'default':
            num_clusters = 10
        elif int(num_clusters) < 10:
            print("'num_clusters' parameter too low, defaulting to 10.")
            num_clusters = 10
        else:
            num_clusters = int(num_clusters)
            
    else: 
        raise ValueError("'pattern_order' parameter not supported by pattern_orientation().")
    
    response2D = response.reshape(-1, response.shape[-1])
    
    # clustering 
    t1 = time.time()
    print("Performing k-means clustering, this may take a while...")
    centroids = kmeans(response2D, num_clusters)[0]
    clusterMembers1D, dists1D = vq(response2D, centroids)
    clusterMembers2D = clusterMembers1D.reshape(response.shape[0:2]) 
    
    t2 = time.time() - t1
    print(f"Clustering runtime = {t2:0.3} s")

    # get inputs of selected clusters
    clusterMembers2DTrim = trimage(clusterMembers2D, l)
    plt.imshow(clusterMembers2DTrim, cmap='jet')
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
        cluster = clusterMembers2DTrim[y, x] 

        if cluster not in selected_clusters:
            selected_clusters.append(cluster)
            # mask out the cluster from non-trimmed data, clusterMembers2D
            defects += np.where(clusterMembers2D == int(cluster), 1, 0)
    
    # compute defect response distance
    defects = defects * dists2D
    
    return centroids, clusterMembers2D, defects 


def orientation(pattern_order, l, response, orients):
    r""" Finds the local pattern orientation using shapelet 
         orientation at max response via an iterative scheme from [1].

    Parameters
    ----------
    pattern_order : str
        Pattern order. Options are: 'stripe', 'square', 'hexagonal'.
    l : float
        The characteristic wavelength of the image.
    response : np.ndarray
        The 3D array corresponding to the response of the convolution for a 
        range of shapelets, obtained from shapelet_response().
    orients : np.ndarray
        The 3D array corresponding to the orientation at max response,
        obtained from shapelet_response().

    Returns
    -------
    mask : np.ndarray
        The mask for well-defined features. See [1].
    dilate : np.ndarray
        The dilated mask. See [1].
    orientation : np.ndarray
        Applying smoothing/blending to the dilated mask via median filter kernel [2]. See [1].
    maxval : float
        The maximum allowed orientation value, where maxval = 2*np.pi / (m)

    Notes
    -----

    References
    ----------
    .. [1] TODO: REFTINO
    .. [2] https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.median_filter.html

    Examples
    --------
    
    """
    params = {
        'stripe': 0,
        'square': 3, 
        'hexagonal': 5
    }

    if pattern_order not in params:
        raise ValueError("'pattern_order' parameter not supported by pattern_orientation().")
    ind = params[pattern_order]
    maxval = 2*np.pi / (ind+1)
        
    # find the response threshold iteratively 
    orient = orients[:,:,ind].copy()
    resp_og = response[:,:,ind].copy()
    dilationsize = int( np.round(2*l, 0) )
    blendsize = int( np.round(4*l, 0) )
    
    accept_solution = False
    resptol = 1.0
    errtol = 0.01
    
    print(f"Beginning iteration with response tolerance = {errtol}\n")
    while not accept_solution:
        resp = np.where(resp_og > resptol, 1, 0)
        mask = trimage((orient * resp), l)
        
        dilate = grey_dilation(mask, size=dilationsize)
        orientation = median_filter(dilate, size=blendsize)
    
        # compute error on undefined values after blending
        err = (orientation == 0.0).sum() / orientation.size
            
        if err > errtol:
            #TODO: alex@matthew: adaptive step width for resptol
            resptol -= 0.01
            resptol = np.round(resptol, 2)
            print(f"Orientation failed with error {err:0.5}. Reducing threshold to {resptol}")
        elif resptol < 0:
            raise RuntimeError('Orientation failed to produce plot.')
        else:
            print(f"Orientation successful with error {err:0.5}")
            accept_solution = True  

    return mask, dilate, orientation, maxval


def rdistance(image, response, num_clusters, ux, uy):
    r""" Compute the response distance method from [1] using the
         methodology described in [2, 3].

    Parameters
    ----------
    image : numpy.ndarray
        The image loaded as a numpy array.
    response : np.ndarray
        The 3D array corresponding to the response of the convolution for a 
        range of shapelets, obtained from shapelet_response()
    num_clusters : int
        The number of clusters as input to k-means clustering [4].
    ux : list (or str if 'default')
        The bounds in the x-direction for the reference region.
    uy : list (or str if 'default')
        The bounds in the y-direction for the reference region.

    Returns
    -------
    d : np.ndarray
        The response distance scalar field.

    Notes
    -----

    References
    ----------
    .. [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    .. [2] https://doi.org/10.1088/1361-6528/aaf353
    .. [3] TODO: REFTINO
    .. [4] https://doi.org/10.1007/978-3-642-29807-3

    Examples
    --------

    """
    if num_clusters == 'default': num_clusters = 20
    else: num_clusters = int(num_clusters)

    if ux == 'default' or uy == 'default': choose_ref = True
    else: choose_ref = False

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
        
    # compute response distance
    Ny, Nx = response.shape[0], response.shape[1]
    uX, uY = np.meshgrid(np.arange(ux[0], ux[1] + 1), np.arange(uy[0], uy[1] + 1))
    response_ref_whole = response[uY, uX] 
    response_ref_whole = response_ref_whole.reshape( -1, response_ref_whole.shape[-1] )

    if num_clusters != 0:
        response_ref, distortion = kmeans(response_ref_whole, num_clusters)
        print(f"kmeans successful with {num_clusters} centroids & distortion value of: {distortion:0.3}")
    else:
        response_ref = response_ref_whole.copy()
        print("Proceeding to compute response distance without k-means clustering:")

    t1 = time.time()
    d = np.zeros((Ny, Nx))
    compList = np.array([10, 25, 50, 75, 100]).astype(int)
    for i in range(Nx):
        if int(100* i / Nx) in compList:
            compList = compList[1:]
            print(f"Response distance {int(100* i / Nx)}% complete")
        for j in range(Ny):
            dists = np.zeros(response_ref.shape[0])
            for refvec in range(response_ref.shape[0]):
                dists[refvec] = np.linalg.norm(response[j, i] - response_ref[refvec])
            d[j, i] = dists.min()
    print("Response distance 100% complete")
    
    print(f"Response distance runtime = {time.time()-t1:0.3} s")

    return d