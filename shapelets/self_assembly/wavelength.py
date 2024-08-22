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

import numbers 

import numpy as np

__all__ = [
    'get_wavelength',
    'radialavg',
]


def get_wavelength(image: np.ndarray, rng: list = [0, 70], verbose: bool = True) -> float:
    r""" 
    Find characteristic wavelength of an image. Computed using method described in ref.[1]_.
    
    Parameters
    ----------
    * image: np.ndarray
        * The image to be processed
    * rng: list
        * Range of wavelengths to consider for maximum wavelength. I.e., will return max wavelength in range of [0, 70] (default)

    Returns
    -------
    * char_wavelength: float
        * The characteristic wavelength of the image

    References
    ----------
    .. [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    
    """
    if type(image) != np.ndarray:
        raise TypeError('image input must be numpy array.')

    # Step 1: Find spectral density
    DFT = np.fft.fft2(image)
    DFT[0, 0] = 0.1
    # Shift the Fourier transform to center it
    DFT_shifted = np.fft.fftshift(DFT)
    # Calculate the magnitude
    spec_d = np.absolute(DFT_shifted)
    
    # Step 2: Find associated frequencies for spectral density
    x, y = np.fft.fftfreq(image.shape[1]), np.fft.fftfreq(image.shape[0])
    # Meshgrid them to map over the image domain
    X, Y = np.meshgrid(x, y)
    # Convert to 2d frequency definition (2.16 in [2]), shift and return
    omega = np.sqrt(X**2 + Y**2)
    freqs = np.fft.fftshift(omega)
    
    # Step 3: Find the radially averaged spectral density, and associated frequencies
    rai_spec = radialavg(spec_d)
    # Use inverse of frequency for wavelength
    rai_wave = radialavg(freqs)
    rai_wave = rai_wave ** -1
    
    # Step 4: Find and return the maximum
    if rng is not None:
        rai_spec = np.where((rai_wave >= rng[0]) * (rai_wave <= rng[1]), rai_spec, 0)
    i_max = rai_spec.argmax()
    
    if verbose:
        print('Wavelength of image is {:.2f} pixels'.format(rai_wave[i_max]))
    
    assert isinstance(rai_wave[i_max], numbers.Real)
    
    return rai_wave[i_max]

def radialavg(image: np.ndarray) -> np.ndarray:
    r""" 
    Calculates the radially averaged intensity of an image. Based on work from ref.[1]_.
    
    Parameters
    ----------
    * image: np.ndarray
        * The image to be radially averaged
    
    Returns
    -------
    * rai: np.ndarray
        * A 1d array with one intensity per integer radius, excluding 0. eg. For image with radii [0, 1, 2, 3], len(rai) = 3

    References
    ----------
    .. [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    
    """
    # Determine two arrays, x and y, which contain the indices of the image.
    y, x = np.indices(image.shape[0:2])
    # Determine the center of the image.
    center = np.array([(x.max()-x.min())/2.0, (y.max()-y.min())/2.0])
    # Use the center to offset x and y such that r = 0 is in the center (0, 0).
    x = x - center[0]
    y = y - center[1]
    # Determine the shortest dimension, as the radius is only defined for that range.
    length = min(np.max(x), np.max(y))
    # Scale x and y based on the radial range. This method creates an elliptical average for non-square images.
    x = x * length / np.max(x) 
    y = y * length / np.max(y)
    # Convert from x and y to radius using the hypotenuse definition.
    r = np.hypot(x, y)
    # Flatten the radius array and sort the radii, returning the indices. Uses quicksort.
    ind = np.argsort(r.flat)
    # Cast r values and image values to 1d arrays, sorted by radius.
    r_sorted = r.flat[ind]
    image_sorted = image.flat[ind]
    # Round the radii to the nearest even number and cast to int.
    r_int = np.around(r_sorted).astype(int)
    # Calculate the spacing between each radii
    deltar = r_int[1:] - r_int[:-1] # Suderman: "Assumes all radii represented"
    # Return the indices for values of delta that are non-zero. This will be the places where (before) r changes.
    rind = np.where(deltar)[0]
    # Append rind such that the last radii is represented
    rind = np.append(rind, len(r_int) - 1)
    # Determine number of items in each bin by taking the difference between indices where the bins change.
    nr = rind[1:] - rind[:-1]
    # Compute an array for the cumulative sum of a_sorted.
    csim = np.cumsum(image_sorted, dtype=float)
    # Take the difference between cumulative sums to determine the sum of image intensities for each bin.
    tbin = csim[rind[1:]] - csim[rind[:-1]]
    # Divide the sum of the bin by the number in each bin, giving a radial average intensity for each radius.
    rai = tbin / nr
    
    return rai