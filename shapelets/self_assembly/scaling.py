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

import numpy as np

from .kernel import get_opt_kernel_n1

__all__ = [
    'lambda_to_beta_n0',
    'lambda_to_beta_n1',
]


def lambda_to_beta_n0(m: int, l: float) -> float:
    r""" 
    Converts lambda (l), the characteristic wavelength of the image [1] to the appropriate beta value for orthonormal polar shapelets [2] with $n=0$ (see shapelets.functions.orthonormalpolar2D_n0).
    
    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry
    * l: float
        * The characteristic wavelength of the image [1]
    
    Returns
    -------
    * beta: float
        * The characteristic shapelet length scale parameter based on ref. [2]

    References
    ----------
    * [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    * [2] https://doi.org/10.1088/1361-6528/aaf353

    """
    if m == 4:   
        f = np.sqrt(2) / 2
    elif m == 3: 
        f = 1 / np.sqrt(3)
    elif m == 2: 
        f = 1 / 2
    elif m == 1: 
        f = 1 / 4
    else:        
        f = 1

    beta = (l / np.sqrt(m)) * f
    return beta

def lambda_to_beta_n1(m: int, l: float, verbose=False) -> float:
    r""" 
    Converts lambda (l), the characteristic wavelength of the image [1] to the appropriate beta value for orthonormal polar shapelets [2] with $n=1$ (see shapelets.functions.orthonormalpolar2D_n1).
    
    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry
    * l: float
        * The characteristic wavelength of the image [1]
    
    Returns
    -------
    * beta: float
        * The characteristic shapelet length scale parameter based on ref. [2]

    References
    ----------
    * [1] http://dx.doi.org/10.1103/PhysRevE.91.033307
    * [2] https://hdl.handle.net/10012/20779

    """
    lambda_opt = np.round(l*1.5, 0)
    beta = 1

    accept = False

    while not accept:

        # get appropriate sized kernel
        shapelet = get_opt_kernel_n1(m = m, beta = beta)

        # extract the midline to work with 1D data for simplicity
        halfpoint = int((shapelet.shape[0] - 1) / 2)
        data = np.real(shapelet[halfpoint, :])

        # now find the two peaks associated with two max / min of inner/outer shapelet lobes
        numpts = data.size
        peak_ind = np.array([])
        for p in range(halfpoint+1, numpts-1): # check all points except for the ends
            if (data[p-1] < data[p] > data[p+1]) or (data[p-1] > data[p] < data[p+1]):
                peak_ind = np.append(peak_ind, p)

        if peak_ind.size != 2:
            print("Error in expected number of peaks... kernel error. Skipping iteration...")
            breakpoint()
            beta += 2*0.1

        else:
            # want {peak_HP - halfpoint} to be close to 1.5*lambda
            peak_MP = np.round((peak_ind[1] - peak_ind[0]) / 2, 0) + peak_ind[0]
            distance = peak_MP - halfpoint
            reldistance = lambda_opt - distance
            if verbose:
                print(f"Current distance {distance}, target is {lambda_opt}")

            ## evaluate acceptability of solution ##

            # found solution
            if np.abs(reldistance) <= 1:
                beta_opt = beta
                if verbose: print(f"optimum beta found to be {beta_opt}")
                accept = True # stop

            # undershot solution
            if reldistance > 0:
                # adaptive stepping to speed up computations
                if reldistance < 2:
                    beta += 0.1
                else: 
                    beta += 3*reldistance * 0.1

            # overshot solution
            elif reldistance < 0:
                if verbose:
                    print("We have overshot target, iterating backwards.")
                beta -= reldistance*0.1
    
    return beta_opt