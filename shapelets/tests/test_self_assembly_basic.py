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
    lambda_to_beta_n0
)

class TestSelfAssemblyBasic(unittest.TestCase):
    r"""
    Unit tests in support of more advanced functionality of shapelets.self_assembly sub-module.
    Uses two simulated images of nanostructure, lamSIM1.png and hexSIM1.png in ./images for testing.
    Currently includes:
        - self_assembly.misc.read_image, 
        - self_assembly.wavelength.get_wavelength, and
        - self_assembly.wavelength.lambda_to_beta_n0
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir = __file__.replace(os.path.basename(__file__), 'images/')
        cls.lamSIM = read_image(image_name = "lamSIM1.png", image_path = cls.dir, verbose = False)
        cls.hexSIM = read_image(image_name = "hexSIM1.png", image_path = cls.dir, verbose = False)

    # This test will be fun first on purpose
    # Test read_image()
    def test_a_first(self) -> None:
        self.assertTrue(isinstance(self.lamSIM, np.ndarray))
        self.assertEqual(self.lamSIM.min(), -1)
        self.assertEqual(self.lamSIM.max(), 1)
        self.assertEqual(self.lamSIM.shape, (296, 296))

        self.assertTrue(isinstance(self.hexSIM, np.ndarray))
        self.assertEqual(self.hexSIM.min(), -1)
        self.assertEqual(self.hexSIM.max(), 1)
        self.assertEqual(self.hexSIM.shape, (507, 507))
    
    # Test get_wavelength() and lambda_to_beta_n0()
    def test_scale(self) -> None:
        with self.assertRaises(TypeError):
            get_wavelength('')

        lamSIM_wvl = get_wavelength(image = self.lamSIM, verbose = False)
        self.assertTrue(isinstance(lamSIM_wvl, numbers.Real))
        self.assertAlmostEqual(lamSIM_wvl, 10.231, places = 3)

        lamSIM_beta = lambda_to_beta_n0(3, lamSIM_wvl)
        self.assertTrue(isinstance(lamSIM_beta, numbers.Real))
        self.assertAlmostEqual(lamSIM_beta, 3.41, places = 2)

        hexSIM_wvl = get_wavelength(image = self.hexSIM, verbose = False)
        self.assertTrue(isinstance(hexSIM_wvl, numbers.Real))
        self.assertAlmostEqual(hexSIM_wvl, 16.882, places = 3)
        
        hexSIM_beta = lambda_to_beta_n0(6, hexSIM_wvl)
        self.assertTrue(isinstance(hexSIM_beta, numbers.Real))
        self.assertAlmostEqual(hexSIM_beta, 6.89, places = 2)

        #TODO lambda_to_beta_n1


if __name__ == "__main__":
    unittest.main()
