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
import platform
import unittest

import numpy as np

from shapelets.self_assembly import (
    read_image, 
    get_wavelength,
    lambda_to_beta
)

class TestBasic(unittest.TestCase):
    r"""
    Unit tests to support basic functionality of shapelets.self_assembly sub-module.
    Uses two simulated images of nanostructure, lamSIM1.png and hexSIM1.png in ./images for testing.
    Currently includes:
        - reading images via shapelets.self_assembly.read_image,
        - computing the characteristic wavelength of the image via shapelets.self_assembly.get_wavelength, and
        - converting lambda (characteristic wavelength) to beta, the shapelet scale via shapelets.self_assembly.lambda_to_beta
    """

    @classmethod
    def setUpClass(cls) -> None:
        if platform.system() == 'Windows':
            cls.dir = __file__.replace(os.path.basename(__file__), 'images\\')
        else:
            cls.dir = __file__.replace(os.path.basename(__file__), 'images/')
        cls.lamSIM = read_image(image_name = "lamSIM1.png", image_path = cls.dir, verbose = False)
        cls.hexSIM = read_image(image_name = "hexSIM1.png", image_path = cls.dir, verbose = False)

        cls.lamSIM_wvl = get_wavelength(image = cls.lamSIM, verbose = False)
        cls.lamSIM_beta = lambda_to_beta(3, cls.lamSIM_wvl)

        cls.hexSIM_wvl = get_wavelength(image = cls.hexSIM, verbose = False)
        cls.hexSIM_beta = lambda_to_beta(6, cls.hexSIM_wvl)

    def test_read(self) -> None:
        self.assertTrue(isinstance(self.lamSIM, np.ndarray))    
        self.assertEqual(self.lamSIM.min(), -1)
        self.assertEqual(self.lamSIM.max(), 1)
        self.assertEqual(self.lamSIM.shape, (296, 296))

        self.assertTrue(isinstance(self.hexSIM, np.ndarray))
        self.assertEqual(self.hexSIM.min(), -1)
        self.assertEqual(self.hexSIM.max(), 1)
        self.assertEqual(self.hexSIM.shape, (507, 507))
    
    def test_wavelength(self) -> None:
        self.assertAlmostEqual(self.lamSIM_wvl, 10.231, places = 3)
        self.assertAlmostEqual(self.hexSIM_wvl, 16.882, places = 3)

    def test_beta(self) -> None:
        self.assertAlmostEqual(self.lamSIM_beta, 3.41, places = 2)
        self.assertAlmostEqual(self.hexSIM_beta, 6.89, places = 2)
    

if __name__ == "__main__":
    unittest.main()
