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

import os
import unittest

import numpy as np

from shapelets.astronomy.galaxy import(
    load_fits_data,
    Stamp,
    get_postage_stamps,
)
from shapelets.astronomy.misc import (
    get_nspace,
    get_compressed_nspace,
    decompose_kernel,
    reconstruct,
    update_shapelet_parameters
)


class TestAstronomyBasic(unittest.TestCase):
    r""" Unit tests to support functionality of shapelets.astronomy sub-module.
    
    Uses one astronomical data file galaxies.fits and a variety of test cases
    Currently includes tests for:
        - astronomy.galaxy.load_fits_data
        - astronomy.galaxy.get_postage_stamps
        - astronomy.misc.decompose_kernel
        - astronomy.misc.reconstruct
        - astronomy.misc.update_shapelet_parameters
        - astronomy.misc.get_nspace
        - astronomy.misc.get_compressed_nspace
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.dir = __file__.replace(os.path.basename(__file__), 'images/')
        cls.raw_data = load_fits_data(cls.dir+'galaxies.fits')

        assert(type(cls.raw_data) == np.ndarray) # raw_data type must be verified before calling get_postage_stamps
        (galaxy_stamps, _, noiseless_data) = get_postage_stamps(cls.raw_data, SHOW_STAMPS=False, verbose=False)
        assert(type(galaxy_stamps) == list) # must verify that function returns list. type of list elements will be verified in further tests

        cls.galaxy_stamps = galaxy_stamps
        cls.stamp = cls.galaxy_stamps[0]
        cls.data = noiseless_data

    def test_a_nspace(self) -> None:
        # Test get_nspace
        with self.assertRaises(ValueError):
            get_nspace(-1)

        nspace = get_nspace(2)
        self.assertEqual(nspace.__len__(), 6)
        self.assertTrue(isinstance(nspace, np.ndarray))  
        self.assertEqual(nspace.tolist(), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)])
        
        # Test get_compressed_nspace
        with self.assertRaises(ValueError):
            get_compressed_nspace([[3, -2], [1, -4]], -2)

        compressed_nspace = get_compressed_nspace(np.array([[6, -3, 2], [4, -5, 1]]), 4)
        self.assertEqual(compressed_nspace, [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_b_read_image(self) -> None:
        # Test load_fits_data
        self.assertTrue(isinstance(self.raw_data, np.ndarray))    
        self.assertAlmostEqual(self.raw_data.min(), -0.00012, places=4)
        self.assertAlmostEqual(self.raw_data.max(),  0.00688, places=4)
        self.assertEqual(self.raw_data.shape, (512, 512))
        
        # Test get_postage_stamps
        self.assertEqual(self.galaxy_stamps.__len__(), 45)
        self.assertTrue(isinstance(self.stamp, Stamp))
        self.assertEqual((self.stamp.x2 - self.stamp.x1).tolist(), [120, 114])
        self.assertAlmostEqual(self.stamp.xc[0], 179.178, places=2)
        self.assertAlmostEqual(self.stamp.xc[1], 358.287, places=2)

    def test_c_decompose(self) -> None:
        image = self.data[self.stamp.x1[0]:self.stamp.x2[0], self.stamp.x1[1]:self.stamp.x2[1]]

        # Test decompose_kernel
        with self.assertRaises(ValueError):
            decompose_kernel(image, -1, self.stamp.beta, self.stamp.xc - self.stamp.x1)
        
        coefficients = decompose_kernel(image, 4, self.stamp.beta, self.stamp.xc - self.stamp.x1)
        self.assertEqual(coefficients.shape, (5, 5))
        self.assertAlmostEqual(np.max(coefficients),  0.07977, places=4)
        self.assertAlmostEqual(np.min(coefficients), -0.00448, places=4)
        
        # Test update_shapelet_parameters
        with self.assertRaises(ValueError):
            update_shapelet_parameters(coefficients, -1, self.stamp.beta, self.stamp.xc - self.stamp.x1)
        
        updated_parameters = update_shapelet_parameters(coefficients, 4, self.stamp.beta, self.stamp.xc - self.stamp.x1)
        self.assertAlmostEqual(updated_parameters[0], 7.9968, places=4)
        self.assertAlmostEqual(updated_parameters[1][0], 61.209, places=2)
        self.assertAlmostEqual(updated_parameters[1][1], 56.013, places=2)

        # Test reconstruct
        with self.assertRaises(ValueError):
            reconstruct(coefficients, -1, updated_parameters[0], updated_parameters[1], image.shape)
    
        reconstructed = reconstruct(coefficients, 4, updated_parameters[0], updated_parameters[1], image.shape)
        self.assertEqual(reconstructed.shape, (120, 114))


if __name__ == "__main__":
    unittest.main()
