import numpy as np
from . import base
from . import dimensionality


def uniform_az_zd_in_cone(
    prng,
    azimuth_rad,
    zenith_rad,
    min_half_angle_rad,
    max_half_angle_rad,
    size=None,
):
    """
    Draw a random pointing (azimuth, zenith distance) from within a cone.

    Parameters
    ----------
    prng : numpy.random.Generator
        Pseudo random number generator
    azimuth_rad : float
        Azimuth pointing of cone.
    zenith_rad : float
        Zenith distance pointing of cone.
    min_half_angle_rad : float
        Minimum half angle of cone.
    max_half_angle_rad : float
        Maximum half angle of cone.
    size : int or None (default None)
        The size (number) of points to be drawn. Behaviour adopted from
        numpy.random.

    Returns
    -------
    (azimuth, zenith distance) : (float, float)
        In rad. If size is not None, the return values will be array like.
    """
    assert min_half_angle_rad >= 0.0
    assert max_half_angle_rad >= min_half_angle_rad

    # Adopted from CORSIKA
    rd1 = prng.uniform(size=size)
    rd2 = prng.uniform(size=size)

    ct1 = np.cos(min_half_angle_rad)
    ct2 = np.cos(max_half_angle_rad)
    ctt = rd2 * (ct2 - ct1) + ct1
    theta = np.arccos(ctt)
    phi = rd1 * np.pi * 2.0

    # TEMPORARY CARTESIAN COORDINATES
    xvc1, yvc1, zvc1 = base.az_zd_to_cx_cy_cz(
        azimuth_rad=phi, zenith_rad=theta
    )
    # ROTATE AROUND Y AXIS
    cos_zenith = np.cos(zenith_rad)
    sin_zenith = np.sin(zenith_rad)

    xvc2 = xvc1 * cos_zenith + zvc1 * sin_zenith
    yvc2 = yvc1
    zvc2 = zvc1 * cos_zenith - xvc1 * sin_zenith

    # BACK TO SPHERICAL COORDINATES
    tmp_az, zd = base.cx_cy_cz_to_az_zd(cx=xvc2, cy=yvc2, cz=zvc2)

    az = tmp_az + azimuth_rad
    az = base.azimuth_range(azimuth_rad=az)

    return az, zd
