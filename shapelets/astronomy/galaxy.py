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

from dataclasses import dataclass

from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Patch
import numpy as np
import sep

from .misc import *

STAR_SIZE = 31 # crude circle with radius of 3 pixels
STAR_COLOUR = 'lightgreen'
GALAXY_COLOUR = 'red'

REFINE_ITERATIONS = 4

@dataclass
class Stamp:
    r""" 
    Contains the necessary information to extract a celestial object from a given dataset.

    Parameters
    ----------
    * x1: np.ndarray (dtype=int)
        * Coordinate representing the corner of postage stamp closest to origin (inclusive)
    * x2: np.ndarray (dtype=int)
        * Coordinate representing the corner of postage stamp furthest from origin (inclusive)
    * xc: np.ndarray (dtype=float)
        * Representing middle of celestial object in postage stamp
    * beta: float
        * The characteristic shapelet scale that the celestial object will be decomposed at

    """
    x1: np.ndarray
    x2: np.ndarray
    xc: np.ndarray
    beta: float

def decompose_galaxies(galaxy_stamps: list[Stamp], star_stamps: list[Stamp], data: np.ndarray, n_max: int, n_compress: int, output_path: str=None) -> None:
    r"""
    Decomposes a series of galaxies into a reduced shapelet representation.

    Parameters
    ----------
    * galaxy_stamps: list[Stamp]
        * List of stamps for the galaxies in the astronomical image data
    * star_stamps: list[Stamp]
        * List of stamps for the stars in the astronomical image data
    * data: np.ndarray
        * Original astronomical data
    * n_max: int
        * Maximum order of shapelets
    * n_compress: int
        * Length of truncated list of shapelet coefficients used to reconstruct astronomical data
    * output_path: str, optional
        * Folder to store output images. If set to None (default), no images are saved
        
    """
    if output_path == None:
        print("No output path provided, galaxy decomposition comparisons will not be saved.")

    # run shapelet deconvolution on each galaxy stamp
    for stamp in galaxy_stamps:
        print(stamp)
        image = data[stamp.x1[0]:stamp.x2[0], stamp.x1[1]:stamp.x2[1]]
        
        sz = image.shape
        relative_centroid = stamp.xc - stamp.x1
        beta = stamp.beta
        
        # iteratively decompose the image and update the beta and centroid guesses 
        for i in range(REFINE_ITERATIONS):
            print(f"iter {i+1}=> Xc=({relative_centroid[0] :3.2f},{relative_centroid[1] :3.2f}) B={beta :3.2f}")
            s_coeff = decompose_kernel(image, n_max, beta, relative_centroid)
            beta, relative_centroid = update_shapelet_parameters(s_coeff, n_max, beta, relative_centroid)
    
        # reconstruct image with calculated shapelet coefficients
        img1 = reconstruct(s_coeff, n_max, beta, relative_centroid, sz)

        # reconstruct image with reduced set of shapelet coefficients
        compressed_nspace = get_compressed_nspace(s_coeff, n_compress)
        img2 = reconstruct(s_coeff, n_max, beta, relative_centroid, sz, nspace=compressed_nspace)

        if output_path != None:
            create_plots(image, img1, img2, n_compress, f"{output_path}_{stamp.xc[0] :.0f},{stamp.xc[1] :.0f}")
        else:
            create_plots(image, img1, img2, n_compress)

def get_postage_stamps(data: np.ndarray, output_path: str=None, SHOW_STAMPS: bool=True) -> tuple[list[Stamp], list[Stamp]]:
    r"""
    Extracts a list of galaxy image stamps and star image stamps from the provided astronomical image data.

    Parameters
    ----------
    * data: np.ndarray
        * $n\times m$ array of astronomical image data
    * output_path: str, optional
        * Folder to store output images. If set to None (default), no images are saved
    * SHOW_STAMPS: bool, optional
        * If set to True (default) displays astronomical image data with stamps identified
        
    Returns
    -------
    * galaxy_stamp_list: list[Stamp]
        * List of stamps for the galaxies found in the astronomical image data
    * star_stamp_list: list[Stamp]
        * List of stamps for the stars found in the astronomical image data
    * data: np.ndarray
        * $n\times m$ array of astronomical image data, minus the background determined by the ``sep`` python package 

    """
    if output_path == None:
        print("No output path provided, galaxy map image will not be saved")

    size = data.shape
    data = np.array(data)

    bkg = sep.Background(data)
    data = data - bkg

    print('searching for galaxies')
    (objects, segments) = sep.extract(data, 1.5, err=bkg.globalrms, segmentation_map=True)

    if SHOW_STAMPS or output_path != None:
        # prepare data as images for display
        fig, (ax1, ax2) = plt.subplots(1, 2)
        m, s = np.mean(data), np.std(data)
        ax1.imshow(data, cmap='gray', origin='lower')
        ax2.imshow(data, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')

        fig.suptitle('Galaxy Map')
        ax1.set_title('Linear Intensity')
        ax2.set_title('Mean Normalized Intensity')

        fig.legend(
            loc='lower right',
            handles=[Patch(facecolor=GALAXY_COLOUR, label='Galaxy'),
                     Patch(facecolor=STAR_COLOUR, label='Star')])

    galaxy_stamp_list = []
    star_stamp_list = []
    
    # sorts objects from brightest to dimmest
    objects = np.sort(objects, order=['flux'])[::-1]

    for obj in objects:
        inflation = int((obj['a']))
        stamp = Stamp(
            np.array([ max(0, obj['ymin']-inflation), max(0, obj['xmin']-inflation) ]),
            np.array([ min(obj['ymax']+inflation, size[1]), min(obj['xmax']+inflation, size[0]) ]),
            np.array([obj['y'], obj['x']]),
            0.7*(obj['a'])
        )

        if obj['npix'] <= STAR_SIZE:
            # detected object is star
            star_stamp_list.append(stamp)
            colour = STAR_COLOUR
        else:
             # detected object is galaxy
            galaxy_stamp_list.append(stamp)
            colour = GALAXY_COLOUR

        if SHOW_STAMPS or output_path != None:
            # add an ellipse for each object
            e1 = Ellipse(xy=(obj['x'], obj['y']),
                        width=int(6*obj['a']),
                        height=int(6*obj['b']),
                        angle=np.deg2rad(obj['theta']))
            e1.set_facecolor('none')
            e1.set_edgecolor(colour)
            ax1.add_artist(e1)

            e2 = Ellipse(xy=(obj['x'], obj['y']),
                width=int(6*obj['a']),
                height=int(6*obj['b']),
                angle=np.deg2rad(obj['theta']))
            e2.set_facecolor('none')
            e2.set_edgecolor(colour)
            ax2.add_artist(e2)

    print(f"\n found {len(galaxy_stamp_list)} Galaxies, {len(star_stamp_list)} Stars\n")
    
    if output_path != None:
        plt.savefig(f"{output_path}_map.png", format="png")

    fig.text(0.5, 0.05, 'Close figure to Continue', horizontalalignment='center',
             verticalalignment='center', fontsize=8)
    
    if SHOW_STAMPS: 
        plt.show()

    return galaxy_stamp_list, star_stamp_list, data

def load_fits_data(filename: str) -> np.ndarray:
    r"""
    Loads data as numpy.ndarray from provided .fits file.

    Parameters
    ----------
    * filename: str
        * Absolute or relative filepath to .fits file
        
    Returns
    -------
    * data: np.ndarray
        * $n \times m$ array of astronomical image data
    
    Notes
    -----
    Flexible Image Transport System (or FITS) files were designed to standarize the exchange of astronomical image data between observatories[1]_. FITS provides a method to transport arrays and tables of data alongside its related metadata. 
    
    References
    ----------
    .. [1] https://fits.gsfc.nasa.gov/rfc4047.txt

    """
    with fits.open(filename) as hdul:
        hdul.verify("fix")
        data = hdul[0].data
        return data.byteswap(inplace=True).newbyteorder()
    
def create_plots(data: np.ndarray, reconstructed: np.ndarray, reconstructed_compressed: np.ndarray, compression_factor: int, output_path: str=None) -> None:
    r"""
    Displays original data and image reconstructions, alongside the error from projection onto shapelet basis.

    Parameters
    ----------
    * data: np.ndarray
        * Original astronomical data
    * reconstructed: np.ndarray
        * Reconstruction of astronomical data using calculated shapelet coefficients
    * reconstructed_compressed: np.ndarray
        * Reconstruction of astronomical data using truncated list of shapelet coefficients
    * compression_factor: int
        * Length of truncated list of shapelet coefficients used to reconstruct astronomical data
    * output_path: str, optional
        * File_path to save images to. If set to None (default), then fig is not saved
        
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.imshow(data, origin='lower')
    ax1.set_title('Original Data')
    ax1.set_xticklabels(''), ax1.set_yticklabels('')

    ax2.imshow(reconstructed, origin='lower')
    ax2.set_title('Reconstructed Image')
    ax2.set_xticklabels(''), ax2.set_yticklabels('')

    ax3.imshow(reconstructed_compressed, origin='lower')
    ax3.set_title(f'Reconstruction Compressed to {compression_factor} coeffs')
    ax3.set_xticklabels(''), ax3.set_yticklabels('')

    m, s = np.mean(data), np.std(data)
    err = (data-reconstructed_compressed)**2/abs(data)
    m_err, s_err = np.mean(err), np.std(err)
    print(
        f"err min: {np.min(err) :e}, err max: {np.max(err) :e}\n"
        f"err mean: {m_err :e}, err std: {s_err :e}\n"
        f"relative err mean: {abs(m_err)/m :4.2f}%, relative err std: {abs(s_err)/s :4.2f}%\n"
    )

    ax4.imshow(err, cmap='hot', interpolation='nearest', vmin=m_err-s_err, vmax=m_err+s_err, origin='lower')
    ax4.set_title('Error')
    ax4.set_xticklabels(''), ax4.set_yticklabels('')

    if output_path != None:
        plt.savefig(output_path+".png", format="png")

    fig.text(0.5, 0.02, 'Close figure to Continue',  horizontalalignment='center',
             verticalalignment='center', fontsize=8)
    plt.show()
