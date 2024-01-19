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
import os
import unittest

import numpy as np

from shapelets.self_assembly import (
    read_image, 
    get_wavelength,
    convresponse,
    defectid,
    orientation,
    rdistance
)

class TestMethods(unittest.TestCase):
    r"""
    Unit tests in support of more advanced functionality of shapelets.self_assembly sub-module.
    Specifically tests all methods in the self_assembly.quant sub-module.
    Uses one simulated nanostructure image for testing, hexSIM1.png in ./images.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir = __file__.replace(os.path.basename(__file__), 'images/')

        # Ensure core functions have appropriate outputs before proceeding.
        # Note that read_image and get_wavelength are not tested here, so inline asserts
        #   are used to ensure correct output.
        cls.image = read_image(image_name="hexSIM1.png", image_path=cls.dir, verbose=False)
        assert isinstance(cls.image, np.ndarray)

        cls.wvl = get_wavelength(image = cls.image, verbose = False)
        assert isinstance(cls.wvl, numbers.Real)

        cls.omega, cls.phi = convresponse(cls.image, cls.wvl, shapelet_order='default', \
                                          verbose=False)
    
    # This test will be run first on purpose
    def test_a_first(self) -> None:
        self.assertTrue(isinstance(self.omega, np.ndarray))
        self.assertEqual(self.omega.shape, self.image.shape + (10,))

        self.assertTrue(isinstance(self.phi, np.ndarray))
        self.assertEqual(self.phi.shape, self.image.shape + (10,))

    def test_convresponse(self) -> None:
        with self.assertRaises(TypeError):
            convresponse([], self.wvl, shapelet_order='default')

        with self.assertRaises(ValueError): 
            convresponse(self.image, self.wvl, shapelet_order='')
        with self.assertRaises(TypeError):
            convresponse(self.image, self.wvl, shapelet_order=5.)
        
        with self.assertRaises(TypeError):
            convresponse(self.image, self.wvl, shapelet_order='default', \
                         normresponse=[])
        with self.assertRaises(ValueError):
            convresponse(self.image, self.wvl, shapelet_order='default', \
                         normresponse='')

        # Test non-default input of shapelet_order parameter 
        omega, phi = convresponse(self.image, self.wvl, shapelet_order=20, verbose=False)
        self.assertEqual(omega.shape, self.image.shape + (20,))
        self.assertEqual(phi.shape, self.image.shape + (20,))
    
    # Note: cannot test outputs as defectid() is an interactive function.
    def test_defectid(self) -> None:
        with self.assertRaises(TypeError):
            defectid([], self.wvl, 'stripe', 'default')
        
        with self.assertRaises(ValueError):
            defectid(self.omega, self.wvl, 'stripe', '')
        with self.assertRaises(TypeError):
            defectid(self.omega, self.wvl, 'stripe', 5.)

        with self.assertRaises(TypeError):
            defectid(self.omega, self.wvl, [], 'default')
        with self.assertRaises(ValueError):
            defectid(self.omega, self.wvl, 'rectangular', 'default')

    def test_orientation(self) -> None:
        with self.assertRaises(TypeError):
            orientation('hexagonal', self.wvl, [], self.phi)
        with self.assertRaises(TypeError):
            orientation('hexagonal', self.wvl, self.omega, [])

        with self.assertRaises(TypeError):
            orientation([], self.wvl, self.omega, self.phi)
        with self.assertRaises(ValueError):
            orientation('rectangular', self.wvl, self.omega, self.phi)
        
        print(' -> this test may take more than a few seconds')
        mask, dilate, orient_result, _ = orientation('hexagonal', self.wvl, self.omega, \
                                                     self.phi, verbose=False)
        
        self.assertTrue(isinstance(mask, np.ndarray))
        self.assertTrue(isinstance(dilate, np.ndarray))

        self.assertTrue(isinstance(orient_result, np.ndarray))
        err = (orient_result == 0.0).sum() / orient_result.size
        errtol = 0.01 
        self.assertTrue(err <= errtol) # ensure that iteration stopped correctly
    
    def test_rdistance(self) -> None:
        with self.assertRaises(TypeError):
            rdistance([], self.omega, 'default', 'default', 'default')

        with self.assertRaises(TypeError):
            rdistance(self.image, [], 'default', 'default', 'default')
        
        with self.assertRaises(ValueError):
            rdistance(self.image, self.omega, '', 'default', 'default')

        with self.assertRaises(TypeError):
            rdistance(self.image, self.omega, 'default', [1, 2], 'default')
        with self.assertRaises(ValueError):
            rdistance(self.image, self.omega, 'default', 'incorrect', 'default')
        with self.assertRaises(ValueError):
            rdistance(self.image, self.omega, 'default', 'default', 'incorrect')            
        with self.assertRaises(ValueError):
            rdistance(self.image, self.omega, 'default', [1,2,3], [1,2])
        with self.assertRaises(ValueError):
            rdistance(self.image, self.omega, 'default', [1,2], [1,2,3])

        ux, uy = [237, 283], [32, 78]
        print(' -> this test may take more than a few seconds')

        d = rdistance(self.image, self.omega, 'default', ux, uy, verbose=False)

        self.assertTrue(d.shape, self.image.shape)
        self.assertTrue(d.min() >= 0.)
        self.assertTrue(d.max() <= 1.)


if __name__ == "__main__":
    unittest.main()
