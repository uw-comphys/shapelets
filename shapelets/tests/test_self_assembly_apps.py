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

from shapelets.self_assembly.tools import(
    convresponse_n0,
    convresponse_n1,
)
from shapelets.self_assembly.misc import read_image
from shapelets.self_assembly.apps import (
    identify_defects,
    orientation,
    response_distance,
)


class TestSelfAssemblyApps(unittest.TestCase):
    r""" Unit tests in support of more advanced functionality of shapelets.self_assembly sub-module.
    
    Specifically tests all applications in the self_assembly.apps sub-module.
    Uses one simulated nanostructure image for testing, hexSIM1.png in ./images.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.dir = __file__.replace(os.path.basename(__file__), 'images/')

        # Ensure core functions have appropriate outputs before proceeding.
        # NOTE: read_image & get_wavelength are not tested here, so inline asserts are used to ensure correct output.
        
        cls.image = read_image(image_name="hexSIM1.png", image_path=cls.dir, verbose=False)

        assert isinstance(cls.image, np.ndarray)

        cls.omega, cls.phi = convresponse_n0(cls.image, shapelet_order='default', verbose=False)
    
    # This test will be run first on purpose
    def test_a_responses(self) -> None:
        self.assertTrue(isinstance(self.omega, np.ndarray))
        self.assertEqual(self.omega.shape, self.image.shape + (10,))

        self.assertTrue(isinstance(self.phi, np.ndarray))
        self.assertEqual(self.phi.shape, self.image.shape + (10,))

    def test_convresponse_n0(self) -> None:
        with self.assertRaises(TypeError):
            convresponse_n0([], shapelet_order='default')

        with self.assertRaises(ValueError): 
            convresponse_n0(self.image, shapelet_order='')
        with self.assertRaises(TypeError):
            convresponse_n0(self.image, shapelet_order=5.)
        with self.assertRaises(ValueError):
            convresponse_n0(self.image, shapelet_order=-1)

        # Test non-default input of shapelet_order parameter 
        omega, phi = convresponse_n0(self.image, shapelet_order=20, verbose=False)
        self.assertEqual(omega.shape, self.image.shape + (20,))
        self.assertEqual(phi.shape, self.image.shape + (20,))
    
    def test_convresponse_n1(self) -> None:
        with self.assertRaises(TypeError):
            convresponse_n1([], mmax=5)

        with self.assertRaises(TypeError):
            convresponse_n1(self.image, mmax=5.2)
        with self.assertRaises(ValueError):
            convresponse_n1(self.image, mmax=-1)
        
        # Test for arbitrary number of shapelets
        omega, phi = convresponse_n1(self.image, mmax=6, verbose=False)
        self.assertEqual(omega.shape, self.image.shape + (6,))
        self.assertEqual(phi.shape, self.image.shape + (6,))
    
    # Note: cannot test outputs as identify_defects() is an interactive function.
    def test_identify_defects(self) -> None:
        with self.assertRaises(TypeError):
            identify_defects([], pattern_order='stripe')
        
        with self.assertRaises(ValueError):
            identify_defects(self.image, pattern_order='')
        with self.assertRaises(TypeError):
            identify_defects(self.image, pattern_order=1.)

    def test_orientation(self) -> None:
        with self.assertRaises(TypeError):
            orientation([], pattern_order='square')

        with self.assertRaises(ValueError):
            orientation(self.image, pattern_order='')
        with self.assertRaises(TypeError):
            orientation(self.image, pattern_order=1.)
        
        mask, dilate, orient_result, _ = orientation(self.image, pattern_order='hexagonal', verbose=False)
        
        self.assertTrue(isinstance(mask, np.ndarray))
        self.assertTrue(isinstance(dilate, np.ndarray))

        self.assertTrue(isinstance(orient_result, np.ndarray))
        err = (orient_result == 0.0).sum() / orient_result.size
        errtol = 0.01 
        self.assertTrue(err <= errtol) # ensure that iteration stopped correctly
    
    def test_response_distance(self) -> None:
        with self.assertRaises(TypeError):
            response_distance([])
        with self.assertRaises(ValueError):
            response_distance(self.image, num_clusters=-1)
        with self.assertRaises(TypeError):
            response_distance(self.image, num_clusters=1.)

        with self.assertRaises(TypeError):
            response_distance(self.image, num_clusters=20, ux=[1, 2], uy='default')
        with self.assertRaises(ValueError):
            response_distance(self.image, num_clusters=20, ux='incorrect', uy='default')
        with self.assertRaises(ValueError):
            response_distance(self.image, num_clusters=20, ux='default', uy='incorrect')
        with self.assertRaises(ValueError):
            response_distance(self.image, num_clusters=20, ux=[1,2,3], uy=[1,2])
        with self.assertRaises(ValueError):
            response_distance(self.image, num_clusters=20, ux=[1,2], uy=[1,2,3])

        ux, uy = [237, 283], [32, 78]

        d = response_distance(self.image, num_clusters=20, ux=ux, uy=uy, verbose=False)

        self.assertTrue(d.shape, self.image.shape)
        self.assertTrue(d.min() >= 0.)
        self.assertTrue(d.max() <= 1.)


if __name__ == "__main__":
    unittest.main()
