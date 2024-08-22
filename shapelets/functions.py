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

from typing import Union

import numpy as np
from scipy.special import factorial, genlaguerre, hermite

__all__ = [
    'cartesian1D',
    'cartesian2D',
    'polar2D',
    'orthonormalpolar2D_n0',
    'orthonormalpolar2D_n1',
    'exponential1D',
    'exponential2D'
]

def cartesian1D(n: int, x1: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    1D cartesian shapelet function defined as[AF_cartesian1D]_,

    $$ S_{n}(x; \beta) = \beta^{-\frac{1}{2}}  \phi_{n}(\frac{x}{\beta}) $$

    with $$ \phi_n(x) = \left( 2^n \pi^{\frac{1}{2}} n! \right)^{-\frac{1}{2}} H_n(x) exp(-\frac{x^2}{2}) $$

    where $\phi_n$ is the dimensionless basis function, $\beta$ is the shapelet length scale, $H_n$ is a hermite polynomial of order $n$, and $n$ is the shapelet order parameter.

    Parameters
    ----------
    * n: int
        * Shapelet order. Acceptable values are $n \geq 0$
    * x1: Union[float,np.ndarray]
        * The input to the shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1)

    References
    ----------
    .. [AF_cartesian1D] https://doi.org/10.1046/j.1365-8711.2003.05901.x

    """
    if n < 0:
        raise ValueError('n must be a non-negative integer.')

    # Generate Hermite polynomial
    H = hermite(n)

    # Define common expressions
    a = 1 / (( 2**n * np.sqrt(np.pi) * factorial(int(n), exact = True) )**0.5)

    # Define shapelet
    Sc = lambda x: (1/np.sqrt(beta)) * a * H(x/beta) * np.exp(- ((x/beta)**2) / 2 )

    return Sc(x1)

def cartesian2D(n1: int, n2: int, x1: Union[float,np.ndarray], x2: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    2D cartesian shapelet function defined as[AF_cartesian2D]_,

    $$ S_{n_1,n_2}(x_1, x_2; \beta) = \beta^{-1} \phi_{n_1}(\frac{x_1}{\beta}) \phi_{n_2}(\frac{x_2}{\beta}) $$

    with $$ \phi_n(x) = \left( 2^n \pi^{\frac{1}{2}} n! \right)^{-\frac{1}{2}} H_n(x) exp(-\frac{x^2}{2}) $$

    where $\phi_n$ is the dimensionless basis function, $\beta$ is the shapelet length scale, $H_n$ is a hermite polynomial of order $n$, and $n_1$ and $n_2$ are the shapelet orders.

    Parameters
    ----------
    * n1: int
        * Shapelet order in x direction. Acceptable values are $n1 \geq 0$
    * n2: int
        * Shapelet order in y direction. Acceptable values are $n2 \geq 0$
    * x1: Union[float,np.ndarray]
        * First input to shapelet function
    * x2: Union[float,np.ndarray]
        * Second input to shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1, x2): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1, x2)

    References
    ----------
    .. [AF_cartesian2D] https://doi.org/10.1046/j.1365-8711.2003.05901.x

    """
    if n1 < 0 or n2 < 0:
        raise ValueError('n1 and n2 must both be non-negative integers.')

    # Generate Hermite polynomials
    H1 = hermite(n1)
    H2 = hermite(n2)

    # Define common expressions
    a1 = 1 / (( 2**n1 * np.sqrt(np.pi) * factorial(int(n1), exact = True) )**0.5)
    a2 = 1 / (( 2**n2 * np.sqrt(np.pi) * factorial(int(n2), exact = True) )**0.5)

    # Define shapelet
    Sc = lambda x,y: (1/beta) * a1 * H1(x/beta) * np.exp(-((x/beta)**2) / 2 ) \
                    * a2 * H2(y/beta) * np.exp(-((y/beta)**2) / 2)

    return Sc(x1, x2)

def polar2D(n: int, m: int, x1: Union[float,np.ndarray], x2: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    2D polar shapelet function defined as[RM_polar2D]_,

    $$ S_{n, m}(r, \theta; \beta) = \alpha_1 \alpha_2 r^{|m|} L_{(n-|m|)/2}^{|m|} \left(\frac{r^2}{\beta^2}\right) exp\left( -\frac{r^2}{2\beta^2} \right) exp(-im\theta) $$

    with 
    $$ \alpha_1 = \frac{(-1)^{(n-|m|)/2}}{\beta^{|m|+1}} $$
    $$ \alpha_2 = \left[ \frac{[(n-|m|)/2]!} {\pi[(n+|m|)/2]!} \right]^{\frac{1}{2}}  $$

    where $\beta$ is the shapelet length scale, $L$ is the generalized (associated) laguerre polynomial[LP_polar2D]_, $n$ is the shapelet order, and $m$ is also the shapelet order.

    Parameters
    ----------
    * n: int
        * Shapelet order. Acceptable values are $n \geq 0$
    * m: int
        * Also describes shapelet order. Acceptable values $m \in [-n, n]$. However, if n is odd/even, m must also be odd/even respectively
    * x1: Union[float,np.ndarray]
        * First input to shapelet function
    * x2: Union[float,np.ndarray]
        * Second input to shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1, x2): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1, x2)

    References
    ----------
    .. [RM_polar2D] https://doi.org/10.1111/j.1365-2966.2005.09453.x
    .. [LP_polar2D] https://scipy.github.io/devdocs/reference/generated/scipy.special.genlaguerre.html

    """
    if n < 0:
        raise ValueError('n must be a non-negative integer.')
    elif abs(m) > n:
        raise ValueError('m must be between -n and n.')
    elif n % 2 == 0 and m % 2 != 0:
        raise ValueError('m must be even if n is even.')
    elif n % 2 != 0 and m % 2 == 0:
        raise ValueError('m must be odd if n is odd.')

    # Define common expressions
    nm = (n - np.abs(m))/2
    nm2 = (n + np.abs(m))/2

    # Generate Laguerre polynomial
    L = genlaguerre(nm, np.abs(m))

    # Calculate the weighting constant
    c =  ( (-1)**nm / (beta**(np.abs(m)+1)) )  \
        * np.sqrt(factorial(int(nm), exact = True)) \
        / (np.pi * factorial(int(nm2), exact = True) )

    # Define shapelet
    Sp = lambda r,t: c * r**np.abs(m) * L((r/beta)**2) * np.exp(-((r/beta)**2)/2) * np.exp(-1j*m*t)
    Sc = lambda x,y: Sp(np.sqrt(x**2 + y**2), np.arctan2(y,x))

    return Sc(x1, x2)

def orthonormalpolar2D_n0(m: int, x1: Union[float,np.ndarray], x2: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    Orthonormal 2D polar shapelet function defined as[TA_orthonormalpolar2D_n0]_,

    $$ S_{m}(r, \theta; \beta) = \frac{1}{\beta \sqrt{\pi m!}} \left( \frac{r}{\beta} \right)^m exp \left( -\frac{r^2}{2\beta^2}-im\theta \right) $$

    with $$ \beta = \frac{fl}{\sqrt{m}} $$, and

    where $\beta$ is the shapelet length scale, $f$ is a geometric scale factor[TA_orthonormalpolar2D_n0]_, $l$ is the characteristic wavelength of the image[RS_orthonormalpolar2D_n0]_, and $m$ is the shapelet degree of rotational symmetry.

    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry. Acceptable values are $m > 1$
    * x1: Union[float,np.ndarray]
        * First input to shapelet function
    * x2: Union[float,np.ndarray]
        * Second input to shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1, x2): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1, x2)

    Notes
    -----
    This orthonormal shapelet framework[TA_orthonormalpolar2D_n0]_ was developed for $n = 0$ polar shapelets[RS_orthonormalpolar2D_n0]_. See ref.[RS_orthonormalpolar2D_n0]_ for computing the characteristic wavelength of an image. Note that this shapelet formulation is a re-parameterization of the shapelets.functions.polar2D function.

    References
    ----------
    .. [TA_orthonormalpolar2D_n0] https://doi.org/10.1088/1361-6528/aaf353
    .. [RS_orthonormalpolar2D_n0] http://dx.doi.org/10.1103/PhysRevE.91.033307

    """
    if m < 1:
        raise ValueError("Function only supports m >= 1.")

    # Generate Laguerre polynomial
    n = 0
    L = genlaguerre(n, m)

    # weighting constant
    c = 1 / (np.sqrt(np.pi * factorial(m)))

    # shapelet function
    X = lambda r: r**m * L(r**2) * np.exp(-r**2 / 2)
    Sp = lambda r,t: beta**-1 * c * X(r/beta) * np.exp(-1j*m*t)
    Sc = lambda x,y: Sp(np.sqrt(x**2 + y**2), np.arctan2(y,x))

    return Sc(x1, x2)

def orthonormalpolar2D_n1(m: int, x1: Union[float,np.ndarray], x2: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    Orthonormal 2D polar shapelet function one degree of radial symmetry defined as[MT_orthonormalpolar2D_n1]_,

    $$ S_{m}(r, \theta; \beta) = \frac{r^m \beta^{-(m+1)}}{\sqrt{\pi m! (m+1)}}
                                \left[ 1 + m- \left( \frac{r}{\beta}\right)^2 \right] 
                                e^{-\frac{r^2}{2\beta^2}} e^{-im\theta} $$

    with $$ \beta $$ computed numerically[1]_, and

    where $\beta$ is the shapelet length scale, $l$ is the characteristic wavelength of the image[RS_orthonormalpolar2D_n1]_, and $m$ is the shapelet degree of rotational symmetry.

    Parameters
    ----------
    * m: int
        * Shapelet degree of rotational symmetry. Acceptable values are $m > 1$
    * x1: Union[float,np.ndarray]
        * First input to shapelet function
    * x2: Union[float,np.ndarray]
        * Second input to shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1, x2): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1, x2)

    Notes
    -----
    This orthonormal shapelet framework[MT_orthonormalpolar2D_n1]_ was developed for $n = 1$ polar shapelets[MT_orthonormalpolar2D_n1]_. See ref.[RS_orthonormalpolar2D_n1]_ for computing the characteristic wavelength of an image. Note that this shapelet formulation is a re-parameterization of the shapelets.functions.polar2D function.

    References
    ----------
    .. [MT_orthonormalpolar2D_n1] https://hdl.handle.net/10012/20779
    .. [RS_orthonormalpolar2D_n1] http://dx.doi.org/10.1103/PhysRevE.91.033307

    """
    if m < 1:
        raise ValueError("Function only supports m >= 1.")

    # weighting constant
    c = 1 / ( np.sqrt(np.pi * factorial(m, exact=True) * (m+1)) )

    # shapelet function
    X = lambda r: r**m * (1+m-(r**2)) * np.exp(-0.5 * r**2)
    Sp = lambda r,t: (c / beta) * X(r/beta) * np.exp(-1j*m*t)
    Sc = lambda x,y: Sp(np.sqrt(x**2 + y**2), np.arctan2(y,x))

    return Sc(x1, x2)

def exponential1D(n: int, x1: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r""" 
    1D exponential shapelet function defined as[JB_exponential1D]_,

    $$ S_n(x; \beta) = \alpha \frac{2x}{n\beta} L^{1}_{n-1} \left( \frac{2x}{n\beta} \right) exp\left( -\frac{x}{n\beta} \right) \forall x \geq 0 $$

    with $$ \alpha = \frac{(-1)^{n-1}}{\sqrt{n^3\beta}} $$

    where $\beta$ is the shapelet length scale, $L$ is the generalized (associated) laguerre polynomial[LP_exponential1D]_, and $n$ is the shapelet order.

    Parameters
    ----------
    * n: int
        * Shapelet order. Must be non-negative. Acceptable values are $n \geq 1$
    * x1: Union[float,np.ndarray]
        * The input to the shapelet function. Acceptable values are $x1 \geq 0$
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1)
        
    References
    ----------
    .. [JB_exponential1D] https://doi.org/10.1093/mnras/stz787
    .. [LP_exponential1D] https://scipy.github.io/devdocs/reference/generated/scipy.special.genlaguerre.html

    """
    if n < 1:
        raise ValueError('n must be >= 1.')
    if isinstance(x1, np.ndarray):
        if x1.min() < 0:
            raise ValueError('x1 must only contain values for x >= 0.')
    elif x1 < 0:
        raise ValueError('x1 must be >= 0.')

    # Generate Laguerre polynomial
    L = genlaguerre(n-1, 1)
    # Define common expressions
    a = (-1)**(n-1) / np.sqrt(beta*(n**3))
    # Define shapelet
    Sc = lambda x: a * 2 * x * (n*beta)**-1 * L(2*x/(n*beta)) * np.exp(-x/(n*beta))

    return Sc(x1)

def exponential2D(n: int, m: int, x1: Union[float,np.ndarray], x2: Union[float,np.ndarray], beta: float = 1.) -> Union[float,np.ndarray]:
    r"""
    2D exponential shapelet function defined as[JB_exponential2D]_,

    $$ S_{n,m}(r, \theta; \beta) = \alpha (2r)^{|m|} L^{2|m|}_{n-|m|}\left( \frac{2r}{\beta(2n+1)} \right) exp\left( -\frac{r}{\beta(2n+1)} \right) exp(-im\theta) $$

    with $$ \alpha = \frac{(-1)^n}{(\beta(2n+1))^{|m|}} \sqrt{ \frac{2}{\beta\pi(2n+1)^3} \frac{(n-|m|)!}{(n+|m|)!} } $$

    where $\beta$ is the shapelet length scale, $L$ is the generalized (associated) laguerre polynomial[LP_exponential2D]_, $n$ is the shapelet order, and $m$ is also the shapelet order.

    Parameters
    ----------
    * n: int
        * Shapelet order. Must be non-negative. Acceptable values are $n \geq 0$
    * m: int
        * Also describes shapelet order. Acceptable values are $m \in [-n, n]$
    * x1: Union[float,np.ndarray]
        * First input to shapelet function
    * x2: Union[float,np.ndarray]
        * Second input to shapelet function
    * beta: float
        * The shapelet length scale parameter

    Returns
    -------
    * Sc(x1, x2): Union[float,np.ndarray]
        * Shapelet function evaluated at (x1, x2)

    References
    ----------
    .. [JB_exponential2D] https://doi.org/10.1093/mnras/stz787
    .. [LP_exponential2D] https://scipy.github.io/devdocs/reference/generated/scipy.special.genlaguerre.html

    """
    if n < 0:
        raise ValueError('n must be a non-negative integer.')
    elif np.abs(m) > n:
        raise ValueError('m must be an integer between -n and n.')

    # Define common expressions
    nm = n - np.abs(m)
    nm2 = n + np.abs(m)
    nm3 = (2*n) + 1
    b = 2 / (beta*nm3)

    # Generate Laguerre polynomial
    L = genlaguerre(nm, 2*np.abs(m))
    # Calculate the weighting constant
    c = (-1)**n * np.sqrt(2 * (beta*np.pi)**-1 * nm3**-3) * np.sqrt(factorial(int(nm), exact=True) / factorial(int(nm2), exact=True))

    # Define shapelet
    def Sp(r, t): return c * (r*b)**(np.abs(m)) * L(r*b) * np.exp(-(r/beta) * nm3**-1) * np.exp(-1j*m*t)
    Sc = lambda x,y: Sp(np.sqrt(x**2 + y**2), np.arctan2(y,x))

    return Sc(x1, x2)