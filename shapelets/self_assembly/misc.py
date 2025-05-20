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
This module holds miscellaneous functions for the shapelets.self_assembly module.
"""

import os 

import cv2 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import median_filter

from shapelets.self_assembly.wavelength import get_wavelength


def read_image(
    image_name: str, 
    image_path: str, 
    do_rescale: bool = True, 
    verbose: bool = True
):
    r""" Read an image using OpenCV, with some extra handling. 
    
    By default, re-scales images as greyscale on [-1, 1].
    
    Parameters
    ----------
    image_name : str
        The filename of the image (including extension)
    image_path : str
        The path holding the image
    do_rescale : bool, optional
        Automatically re-scale in accordance with requirements for wavelength algorithm. 
        Default is True
    verbose : bool, optional
        True (default) to print image-related information
    
    Returns
    -------
    f : np.ndarray
        The image as a numpy.ndarray.

    Notes
    -----
    Re-scaling of image to greyscale on [-1, 1] is intentional to align with 
    the minimum and maximum shapelet function values.
    """
    if not os.path.exists(image_path):
        raise RuntimeError(f'Image path: {image_path} does not exist.')
    
    f = cv2.imread(os.path.join(image_path, image_name))
    if not isinstance(f, np.ndarray):
        raise RuntimeError(f"Could not read image: {image_name}. Ensure it is located in {image_path} and is of image format.")

    f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    # NOTE: image may require rescaling based on two observed issues:
    #   1. scipy.cluster.vq.kmeans yields abort: coredump if one dim of image large (~2000 pixels)
    #   2. wavelength algorithm fails if image is too small... need to upsample

    if do_rescale:
        while any(dim >= 2000 for dim in f.shape):
            height, width = round(f.shape[0]*0.8), round(f.shape[1]*0.8)
            f = cv2.resize(f, dsize=(width, height)) # dsize is opposite numpy convention

        while any(dim <= 500 for dim in f.shape):
            height, width = round(f.shape[0]*1.2), round(f.shape[1]*1.2)
            f = cv2.resize(f, dsize=(width, height)) # dsize is opposite numpy convention

    # rescale to [-1, 1] greyscale to match shapelet kernel min/max values
    f = ( ((f-f.min()) / (f.max()-f.min())) * 2 ) - 1

    if verbose: 
        print(f"Successfully loaded image: {image_name}")
        print(f"Image loaded with dimensions: {f.shape}")
        print(f"Image {image_name} normalized to greyscale on [-1, 1] to align with shapelet kernels")

    return f


def process_output(
    image: np.ndarray, 
    image_name: str, 
    save_path: str, 
    output_from: str, 
    **kwargs
):
    r"""  Processes and saves output from any of the functions below,
    shapelets.self_assembly.quant.rdistance,
    shapelets.self_assembly.quant.orientation,
    shapelets.self_assembly.quant.defectid
    
    It was used to generate Figures 6, 7, 8, and 9 [1]_.

    NOTE: any image saved from the **kwargs argument is trimmed using shapelets.self_assembly.misc.trim_image. 
    This is because the convolution with shapelet kernels is padded on the edges, 
    producing a fuzzy convolutional response. trim_image removes this fuzzy response.

    Parameters
    ----------
    image : numpy.ndarray
        The image loaded as a numpy array
    image_name : str
        The name of the loaded image
    save_path : str
        The path to save results
    output_from : str
        The name of the method for which we will process and save the output/results. 
        Options are: 'response_distance', 'orientation', or 'identify_defects'

    Notes
    -----
    Required kwargs are,
    output_from = 'response_distance': d, num_clusters (see shapelets.self_assembly.quant.rdistance)
    output_from = 'orientation': mask, dilate, orientation, maxval (see shapelets.self_assembly.quant.orientation)
    output_from = 'identify_defects': defects, centroids, clusterMembers (see shapelets.self_assembly.quant.defectid)

    References
    ----------
    .. [1] http://dx.doi.org/10.1088/1361-6528/ad1df4
    """
    # check that save_path exists
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        
    os.chdir(save_path)

    # need to get characteristic wavelength for image trimming
    char_wavelength = get_wavelength(image = image, verbose = False)

    if output_from == 'response_distance':
        # get kwargs
        d = kwargs['d']
        num_clusters = kwargs['num_clusters']
        if num_clusters == 'default':
            num_clusters = '20'

        # final image processing for response distance scalar field
        d = (d-d.min()) / (d.max()-d.min())
        d = 1-d
        d = trim_image(im=d, l=char_wavelength)

        # plot and save
        plt.figure()
        plt.imshow(d,cmap='gray')
        plt.axis('off')
        plotname1 = f"{image_name[:-4]}_response_distance_k{num_clusters}.png"
        plt.savefig(fname=plotname1, bbox_inches='tight', pad_inches=0)
        
        plt.figure()
        plt.imshow(trim_image(image,char_wavelength), cmap='gray')
        plt.imshow(d,alpha=0.7, cmap='summer')
        plt.axis('off')
        plotname2 = f"{image_name[:-4]}_response_distance_overlay_k{num_clusters}.png"
        plt.savefig(fname=plotname2, bbox_inches='tight', pad_inches=0)
        print(f"Figure {plotname1} and {plotname2} saved to {save_path}")
    
    elif output_from == 'orientation':
        # get kwargs
        mask = kwargs['mask']
        dilate = kwargs['dilate']
        orientation = kwargs['orientation']
        maxval = kwargs['maxval']
        
        # plot and save
        plt.figure()
        plt.imshow(trim_image(image,char_wavelength), cmap='gray', alpha = 0.5)
        mask[mask == 0.0] = np.nan
        plt.imshow(mask, cmap='hsv', vmin=0, vmax=maxval)
        plt.axis('off')
        plotname1 = f"{image_name[:-4]}_orientation_maskedresp.png"
        plt.savefig(fname=plotname1, dpi=600, bbox_inches='tight', pad_inches=0)
        
        plt.figure()
        plt.imshow(trim_image(image,char_wavelength), cmap='gray')
        plt.imshow(dilate, cmap='hsv', alpha = 0.7, vmin=0, vmax=maxval)
        plt.axis('off')
        plotname2 = f"{image_name[:-4]}_orientation_dilate.png"
        plt.savefig(fname=plotname2, dpi=600, bbox_inches='tight', pad_inches=0)
        
        plt.figure() 
        plt.imshow(orientation, cmap='hsv', vmin=0, vmax=maxval)
        plt.axis('off')
        plotname3 = f"{image_name[:-4]}_orientation_blend.png"
        plt.savefig(fname=plotname3, dpi=600, bbox_inches='tight', pad_inches=0)
        
        plt.figure()
        plt.imshow(trim_image(image,char_wavelength), cmap='gray')
        plt.axis('off')
        im = plt.imshow(orientation, cmap='hsv', alpha = 0.7, vmin=0, vmax=maxval)
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        plt.colorbar(im, cax=cax)
        plotname4 = f"{image_name[:-4]}_orientation_overlay.png"
        plt.savefig(fname=plotname4, dpi=600, bbox_inches='tight', pad_inches=0)
        print(f"Figure {plotname1}, {plotname2}, {plotname3}, and {plotname4} saved to {save_path}")
    
    elif output_from == 'identify_defects':
        # get kwargs
        defects = kwargs['defects']
        centroids = kwargs['centroids']
        clusterMembers = kwargs['clusterMembers']
        
        # apply some smoothing on scale of half lambda
        kernelsize = int(np.round(char_wavelength/2, 0))
        defects = median_filter(defects, size = kernelsize)
        defects = trim_image(defects, char_wavelength) 

        # cluster location image
        plt.close()
        num_clusters = centroids.shape[0]
        clusterMembersTrim = trim_image(clusterMembers, char_wavelength)
        im = plt.imshow(clusterMembersTrim, cmap='jet')
        # get the unique colours of this plot
        values = np.unique(clusterMembersTrim.ravel())
        colours = [ im.cmap(im.norm(value)) for value in values]
        plt.axis('off')
        plotname1 = f"{image_name[:-4]}_defectid_clustloc_k{num_clusters}.png"
        plt.savefig(fname=plotname1, dpi=600, bbox_inches='tight', pad_inches=0)

        # radar chart
        # re-position the clusters so that they are sorted by mean.. for plotting consistency
        numspokes = 7
        mset = np.linspace(1, numspokes, numspokes).astype(int)
        
        # get the xtick labels... but need to repeat first label to complete radar chart (weird)
        categories = []
        for j in range(len(mset)):
            if j == 0: categories.append('m={}'.format(mset[j]))
            else: categories.append('{}'.format(mset[j]))
        categories.append('m={}'.format(mset[0]))
        
        # repeat first cluster value to work with radar charts
        centroids_plot = np.c_[ centroids[:,0:numspokes], centroids[:,0] ]
        
        ax = plt.subplots(1,num_clusters)[1]
    
        for plot in range(num_clusters):
            label_placement = np.linspace(start=0, stop=2*np.pi, num=len(categories))
        
            # handle subplot specifications
            numrows = (num_clusters // 4) + (num_clusters % 4)
            ax[plot] = plt.subplot(numrows, 4, plot+1, polar=True)

            if numrows <= 3:
                xtickpos = 0.55
                fsize = 10
            else:
                xtickpos = 0.66
                fsize = 9    

            ax[plot].set_title(label='Centroid {}'.format(plot), fontsize=fsize)
            ax[plot].set_xticks(label_placement, labels=categories, position=(0,xtickpos), fontsize=fsize)
            ax[plot].set_yticklabels([])
            ax[plot].grid(False)
            ax[plot].set_ylim(0,1.0) # set the radial gridlines to be from 0-1.0
            ax[plot].set_theta_offset(np.pi / 2) # rotate the plot 90 degrees, start from top
            ax[plot].set_theta_direction(-1) # set to CW not CCW
            plt.plot(label_placement, centroids_plot[plot], color=colours[plot])
    
        plt.tight_layout()    
        plotname2 = f"{image_name[:-4]}_defectid_rc_k{num_clusters}.png"
        plt.savefig(fname=plotname2, bbox_inches='tight')

        # defect response distance scalar field
        plt.figure()
        plt.imshow(1-defects,cmap='gray')
        plt.axis('off')    
        plotname3 = f"{image_name[:-4]}_defectid_drd_k{num_clusters}.png"
        plt.savefig(fname=plotname3, dpi=600, bbox_inches='tight', pad_inches=0)
        
        # overlay
        plt.figure()
        image_norm = (image-image.min()) / (image.max()-image.min())
        image_trim = trim_image(image_norm, char_wavelength)
        plt.imshow(image_trim, cmap='gray')
        plt.imshow(defects, cmap = 'gray', alpha = 0.6)
        plt.axis('off')
        plotname4 = f"{image_name[:-4]}_defectid_drd_overlay_k{num_clusters}.png"
        plt.savefig(fname=plotname4, dpi=600, bbox_inches='tight', pad_inches=0)
        print(f"Figure {plotname1}, {plotname2}, {plotname3}, and {plotname4} saved to {save_path}")
    
    else: 
        raise ValueError(f"output_from parameter as {output_from} not recognized by process_output().")


def image_difference(
    im1: np.ndarray, 
    im2: np.ndarray
):
    r""" This function computes the normalized difference between two images. 
    
    It was used to generate Figure 5 [1]_.

    Parameters
    ----------
    im1 : np.ndarray
        The first image
    im2 : np.ndarray
        The second image
        
    Returns
    -------
    diff : np.ndarray
        The normalized difference in the input images

    Notes
    -----
    Only supports input images that are of the same dimensions.
    
    References
    ----------
    .. [1] http://dx.doi.org/10.1088/1361-6528/ad1df4
    """
    if im1.shape != im2.shape:
        raise RuntimeError("Must ensure both images are of same dimensions!")
    
    im1 = (im1-im1.min()) / (im1.max()-im1.min())
    im2 = (im2-im2.min()) / (im2.max()-im2.min())
    print('Scaling pixel intensities between [0, 1] for comparison')

    diff = im2 - im1 
    diff = 1 - ( (diff-diff.min()) / (diff.max()-diff.min()) )
    
    return diff


def trim_image(
    im: np.ndarray, 
    l: float
):
    r""" Trim image edges based on characteristic wavelength (l) [1]_. 
    Useful for images post convolution, as edges can present distortions from padded convolution.

    Parameters
    ----------
    im : np.ndarray
        The image to trim
    l : float
        The characteristic wavelength of the image
    
    Returns
    -------
    trimmed : np.ndarray
        The trimmed image

    Notes
    -----
    The characteristic wavelength is roughly the distance between feature centers, 
    thus making it an appropriate size for image trim or truncation after convolution.

    References
    ----------
    .. [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    """
    trim = round(l/2)
    trimmed = im[trim:-trim, trim:-trim]
    return trimmed
