/**
 * Copyright 2023 the authors (see AUTHORS file for full list).  
 * 
 * This file is part of shapelets. 
 * 
 * Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
 * Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)
 * any later version.
 * 
 * Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
 * details. 
 * 
 * You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see
 * <https://www.gnu.org/licenses/>.  
 */

#include <algorithm>
#include <cmath>
#include <iostream>

/**
 * A simple C++ implementation of the response distance method from ref. [1], developed by Matthew Tino (mptino@uwaterloo.ca).
 * Note that 'extern "C"' must be used such that this function is compiled as C code for use as shared library, in compatibility with ctypes python library. Extra int type parameters are needed because the size of arrays cannot be inferred from pointer.
 * Additionally, to compile this file as shared library: g++ -fPIC -shared -o rdistance.so rdistance.cpp
 * 
 * @param refs Pointer to first element of 2D array refs, which contains the reference response vectors.
 * @param test Pointer to first element of 2D array test, which contains the test (or non-reference) response vectors.
 * @param numrefs Integer referring to the number of reference response vectors.
 * @param numtest Integer referring to the number of test response vectors.
 * @param mmax Integer referring to the maximum m-fold shapelet used for convolutions. This should also equal the number of columns in refs and test, provided that m=0 is not used.
 * 
 * @return final_distances Pointer to first element of 1D array holding the final response distance values. 
 * 
 * [1] https://doi.org/10.1103/PhysRevE.91.033307
 */
extern "C" {
    double* rdistance(double* refs, double* test, int numrefs, int numtest, int mmax) {

        // Allocate array on heap for final response distance values
        double* final_distances = new double[numtest]; 

        // For each test (response) vector
        for (int i = 0; i < numtest; i++) {

            // Allocate array on heap for response distance array
            double* distances = new double[numrefs];

            // For each reference vector
            for (int j = 0; j < numrefs; j++) {

                // Reset summation component of l2 norm for each reference vector
                double accum = 0;
                
                // For each element pair, add to accum the square of the difference
                for (int p = 0; p < mmax; p++) {
                    // Dereference arrays to get specific element value
                    double refval = *((refs + j * mmax) + p); 
                    double testval = *((test + i * mmax) + p);

                    accum += pow(testval - refval, 2);
                }

                // Perform square root to get l2 norm value
                distances[j] = sqrt(accum);
            }

            // Use std::min_element to return minimum value in (unsorted) array
            double* min_distance = std::min_element(distances, distances + numrefs);
            final_distances[i] = *min_distance; // dereference and assignment

            // clear heap memory
            delete[] distances;
        }

        return final_distances;
    }
}


/**
 * Contains sample arrays to test the rdistance() function. Should only be used for testing purposes.
 */
int main() {

    // Declare example reference and test (response) vectors as arrays
    double refs[3][3] = { {2., 5., 9.}, {3., 4., 6.}, {1., 5., 7.} };    
    double test[2][3] = { {3., 4., 8.}, {5., 2., 7.} };

    double* rdistances = rdistance((double*)refs, (double*)test, 3, 2, 3);

    // should expect [1.73205, 3.] as answer (but printed vertically)
    std::cout << *(rdistances) << '\n' << *(rdistances+1) << '\n'; 

    delete[] rdistances; 

    return 0;
}

