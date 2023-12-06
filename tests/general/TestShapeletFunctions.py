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

import unittest

import numpy as np

from shapelets.functions import (
    cartesian1D,
    cartesian2D,
    polar2D,
    orthonormalpolar2D,
    exponential1D,
    exponential2D
)

class TestShapeletFunctions(unittest.TestCase):
    r"""
    Unit tests for the various shapelet function formulations in shapelets/functions.py.
    Currently includes,
        - cartesian shapelets (shapelets.functions.cartesian1D and shapelets.functions.cartesian2D),
        - polar shapelets (shapelets.functions.polar2D),
        - orthonormal polar shapelets (shapelets.functions.orthonormalpolar2D), and
        - exponential shapelets (shapelets.functions.exponential1D and shapelets.functions.exponential2D)
    """

    @classmethod
    def setUpClass(cls) -> None:
        # Define the set of values to test shapelet functions
        cls.xvals = np.array([-1, 0, 1])

    def test_cartesian(self) -> None:
        shapelet1D = cartesian1D(n = 1, x1 = self.xvals)

        self.assertEqual(shapelet1D[1], 0)
        self.assertAlmostEqual(shapelet1D[0], -0.644, places = 3)
        self.assertAlmostEqual(shapelet1D[2], 0.644, places = 3)

        with self.assertRaises(ValueError): 
            cartesian1D(n = -1, x1 = self.xvals)
        
        shapelet2D = cartesian2D(n1 = 2, n2 = 3, x1 = self.xvals, x2 = self.xvals)

        self.assertEqual(shapelet2D[1], 0)
        self.assertAlmostEqual(shapelet2D[0], 0.0847, places = 4)
        self.assertAlmostEqual(shapelet2D[2], -0.0847, places = 4)
        
        with self.assertRaises(ValueError): 
            cartesian2D(n1 = -1, n2 = 0, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            cartesian2D(n1 = 0, n2 = -1, x1 = self.xvals, x2 = self.xvals)
    
    def test_polar(self) -> None:
        shapelet2D = polar2D(n = 1, m = 1, x1 = self.xvals, x2 = self.xvals)

        self.assertTrue(np.iscomplexobj(shapelet2D))

        self.assertEqual(shapelet2D[1], 0)
        self.assertAlmostEqual(np.real(shapelet2D[0]), -0.117, places = 3)
        self.assertAlmostEqual(np.real(shapelet2D[2]), 0.117, places = 3)

        with self.assertRaises(ValueError): 
            polar2D(n = -1, m = 1, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            polar2D(n = 1, m = 2, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            polar2D(n = 2, m = -3, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            polar2D(n = 2, m = 1, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            polar2D(n = 3, m = 2, x1 = self.xvals, x2 = self.xvals)
    
    def test_orthonormal(self) -> None:
        shapelet2D = orthonormalpolar2D(m = 6, x1 = self.xvals, x2 = self.xvals)

        self.assertTrue(np.iscomplexobj(shapelet2D))

        self.assertEqual(shapelet2D[1], 0)
        self.assertAlmostEqual(np.real(shapelet2D[0]), 0., places = 16)
        self.assertAlmostEqual(np.real(shapelet2D[2]), 0., places = 16)

        with self.assertRaises(ValueError): 
            orthonormalpolar2D(m = 0, x1 = self.xvals, x2 = self.xvals)
    
    def test_exponential(self) -> None:
        shapelet1D = exponential1D(n = 1, x1 = self.xvals+1)

        self.assertEqual(shapelet1D[0], 0)
        self.assertAlmostEqual(shapelet1D[1], 0.736, places = 3)
        self.assertAlmostEqual(shapelet1D[2], 0.541, places = 3)

        with self.assertRaises(ValueError): 
            exponential1D(n = 0, x1 = self.xvals+1)
        with self.assertRaises(ValueError): 
            exponential1D(n = 1, x1 = self.xvals)           
        with self.assertRaises(ValueError): 
            exponential1D(n = 1, x1 = -1)  

        shapelet2D = exponential2D(n = 2, m = 2, x1 = self.xvals+1, x2 = self.xvals+1)

        self.assertTrue(np.iscomplexobj(shapelet2D))

        self.assertEqual(shapelet2D[0], 0)
        self.assertAlmostEqual(np.imag(shapelet2D[1]), -0.0035, places = 4)
        self.assertAlmostEqual(np.imag(shapelet2D[2]), -0.011, places = 3)

        with self.assertRaises(ValueError): 
            exponential2D(n = -1, m = 1, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            exponential2D(n = 1, m = 2, x1 = self.xvals, x2 = self.xvals)
        with self.assertRaises(ValueError): 
            exponential2D(n = 2, m = -3, x1 = self.xvals, x2 = self.xvals)


if __name__ == "__main__":
    unittest.main()
        