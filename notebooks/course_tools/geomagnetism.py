"""Spherical-harmonic design matrix used in the geomagnetism notebook."""

import numpy as np
from ppigrf.ppigrf import get_legendre

REFERENCE_RADIUS_M = 6371.2e3


def design_matrix(radius_m, latitude, longitude, maximum_degree):
    """
    Relate internal Gauss coefficients to North, East, Centre components.

    The columns contain first all g(n, m) coefficients, including m = 0,
    and then all h(n, m) coefficients, for which m starts at 1.
    """

    radius_m = np.asarray(radius_m, dtype=float).reshape(-1, 1)
    latitude = np.asarray(latitude, dtype=float).reshape(-1)
    longitude = np.asarray(longitude, dtype=float).reshape(-1)

    if not (radius_m.size == latitude.size == longitude.size):
        raise ValueError("radius, latitude, and longitude must have the same size")

    cosine_keys = tuple((degree, order) for degree in range(1, maximum_degree + 1) for order in range(degree + 1) )
    sine_keys = tuple((degree, order) for degree in range(1, maximum_degree + 1) for order in range(1, degree + 1) )

    theta = np.radians(90 - latitude).reshape(-1, 1)
    phi   = np.radians(longitude).reshape(-1, 1)

    cosine_degree, cosine_order = np.array(cosine_keys).T
    sine_degree, sine_order     = np.array(sine_keys).T

    cosine_degree = cosine_degree.reshape(1, -1)
    cosine_order  = cosine_order.reshape(1, -1)
    sine_degree   = sine_degree.reshape(1, -1)
    sine_order    = sine_order.reshape(1, -1)

    P_cosine, dP_cosine = get_legendre(90 - latitude, cosine_keys)
    P_sine, dP_sine     = get_legendre(90 - latitude, sine_keys)

    radius_ratio = REFERENCE_RADIUS_M / radius_m

    north_cosine  = ( radius_ratio ** (cosine_degree + 2) * dP_cosine * np.cos(cosine_order * phi) )
    east_cosine   = ( radius_ratio ** (cosine_degree + 2) *  P_cosine * cosine_order * np.sin(cosine_order * phi) / np.sin(theta) )
    centre_cosine = (-radius_ratio ** (cosine_degree + 2) * (cosine_degree + 1) * P_cosine * np.cos(cosine_order * phi) )

    north_sine  = ( radius_ratio ** (sine_degree + 2) * dP_sine * np.sin(sine_order * phi) )
    east_sine   = (-radius_ratio ** (sine_degree + 2) *  P_sine * sine_order * np.cos(sine_order * phi) / np.sin(theta) )
    centre_sine = (-radius_ratio ** (sine_degree + 2) * (sine_degree + 1) * P_sine * np.sin(sine_order * phi) )

    north  = np.hstack((north_cosine, north_sine))
    east   = np.hstack((east_cosine, east_sine))
    centre = np.hstack((centre_cosine, centre_sine))

    return np.vstack((north, east, centre)), cosine_keys, sine_keys
