from .version import __version__
import numpy as np


def azimuth_range(azimuth_rad):
    """
    Returns the azimuth in the range of the least absolute residue so that:
        -PI < azimuth_rad <= +PI

    Parameters
    ----------
    azimuth_rad : float
        Azimuth angle.

    Returns
    -------
    azimuth_rad : float
        Azimuth angle.
    """
    PI = np.pi
    TAU = 2.0 * PI
    # force azimuth to be the positive remainder, so that 0 <= angle < TAU
    azimuth_rad = azimuth_rad % TAU
    azimuth_rad = (azimuth_rad + TAU) % TAU
    # force into the minimum absolute value residue class
    # so that: -PI < azimuth <= PI
    if np.isscalar(azimuth_rad):
        if azimuth_rad > PI:
            azimuth_rad -= TAU
    else:
        azimuth_rad = np.asarray(azimuth_rad)
        mask = azimuth_rad > PI
        azimuth_rad[mask] -= TAU
    return azimuth_rad


def az_zd_to_cx_cy_cz(azimuth_rad, zenith_rad):
    """
    Returns the cartesian incident vector for a given incidnet direction in
    azimuth-zenith representation.

    Parameters
    ----------
    azimuth_rad : float
        Azimuth angle of incident.
    zenith_rad : float
        Zenith distance angle of incident.

    Rerturns
    --------
    (cx, cy, cz) : (float, float, float)
        A cartesian vector with length 1.0

    See also the inverse: cx_cy_cz_to_az_zd()
    """
    azimuth_rad = azimuth_range(azimuth_rad=azimuth_rad)
    # Adopted from KIT's CORSIKA
    az = azimuth_rad
    zd = zenith_rad
    cx = np.cos(az) * np.sin(zd)
    cy = np.sin(az) * np.sin(zd)
    cz = np.cos(zd)
    return cx, cy, cz


def az_zd_to_cx_cy(azimuth_rad, zenith_rad):
    """
    Returns the x-y components of a cartesian incident vector (cx, cy) for
    a given incidnet direction in azimuth-zenith representation.

    WARNING
        Pointings below the x-y plane can not be represented this way as
        the z component gets lost. Use az_zd_to_cx_cy_cz() instead when
        pointings might be below the x-y-plane.

    Parameters
    ----------
    azimuth_rad : float
        Azimuth angle of incident.
    zenith_rad : float
        Zenith distance angle of incident.

    Rerturns
    --------
    (cx, cy) : (float, float)
        The x any y components of a cartesian vector with length 1.0

    See also the inverse: cx_cy_to_az_zd()
    And see az_zd_to_cx_cy_cz() for the full vector including the Z component.
    """
    cx, cy, _ = az_zd_to_cx_cy_cz(
        azimuth_rad=azimuth_rad, zenith_rad=zenith_rad
    )
    return cx, cy


def cx_cy_to_az_zd(cx, cy):
    """
    Returns the azimuth-zenith representation for the x-y components of a
    cartesian incident direction vector.

    WARNING
        This assumes that cz is positive, i.e. above the x-y-plane.
        Use cx_cy_cz_to_az_zd() instead when pointings might be below
        the x-y-plane.

    Parameters
    ----------
    cx : float
        X component of cartesian incident direction vector.
    cy : float
        Y component of cartesian incident direction vector.

    Returns
    -------
    (azimuth_rad, zenith_rad) : (float, float)

    See inverse: az_zd_to_cx_cy()
    """

    inner_sqrt = 1.0 - cx**2 - cy**2
    if np.isscalar(inner_sqrt):
        if inner_sqrt >= 0:
            cz = np.sqrt(inner_sqrt)
        else:
            cz = float("nan")
    else:
        cz = np.nan * np.ones(len(inner_sqrt))
        fine = inner_sqrt >= 0
        cz[fine] = np.sqrt(inner_sqrt)
    return cx_cy_cz_to_az_zd(cx=cx, cy=cy, cz=cz)


def cx_cy_cz_to_az_zd(cx, cy, cz):
    """
    Returns the azimuth-zenith representation for a cartesian incident
    direction vector.

    Parameters
    ----------
    cx : float
        X component of cartesian incident direction vector.
    cy : float
        Y component of cartesian incident direction vector.
    cz : float
        Z component of cartesian incident direction vector.

    Returns
    -------
    (azimuth_rad, zenith_rad) : (float, float)

    See inverse: az_zd_to_cx_cy_cz()
    """
    az = np.arctan2(cy, cx)
    zd = arccos_accepting_numeric_tolerance(cz)
    return az, zd


def angle_between_cx_cy_cz(cx1, cy1, cz1, cx2, cy2, cz2):
    """
    Returns the angle between two directions, where the directions are
    represented by cartesian incident direction vectors (cx, cy, cz).

    Parameters
    ----------
    cx1 : float
        X compoonent of 1st.
    cy1 : float
        Y compoonent of 1st.
    cz1 : float
        Z compoonent of 1st.
    cx1 : float
        X compoonent of 2nd.
    cy1 : float
        Y compoonent of 2nd.
    cz1 : float
        Z compoonent of 2nd.

    Returns
    -------
    angle_rad : float
        The angle between the 1st and 2nd direction.
    """
    dot = np.dot
    norm = np.linalg.norm
    norm1 = norm(np.c_[cx1, cy1, cz1], axis=1)
    norm2 = norm(np.c_[cx2, cy2, cz2], axis=1)
    xx = cx1 * cx2
    yy = cy1 * cy2
    zz = cz1 * cz2
    dot12 = np.sum(np.c_[xx, yy, zz], axis=1)
    return arccos_accepting_numeric_tolerance(dot12 / (norm1 * norm2))


def angle_between_cx_cy(cx1, cy1, cx2, cy2):
    """
    See angle_between_cx_cy_cz()

    WARNING
        This assumes all pointings are above the x-y plane.
    """
    cz1 = restore_cz(cx1, cy1)
    cz2 = restore_cz(cx2, cy2)
    return angle_between_cx_cy_cz(cx1, cy1, cz1, cx2, cy2, cz2)


def angle_between_az_zd(azimuth1_rad, zenith1_rad, azimuth2_rad, zenith2_rad):
    """
    Returns the angle between two directions, where the directions are
    represented by azimuth and zenith angles.

    Parameters
    ----------
    azimuth1_rad : float
        Azimuth angle of 1st.
    zenith1_rad : float
        Zenith distance angle of 1st.
    azimuth2_rad : float
        Azimuth angle of 2nd.
    zenith2_rad : float
        Zenith distance angle of 2nd.

    Returns
    -------
    angle_rad : float
        The angle between the 1st and 2nd direction.
    """

    cx1, cy1, cz1 = az_zd_to_cx_cy_cz(
        azimuth_rad=azimuth1_rad, zenith_rad=zenith1_rad
    )
    cx2, cy2, cz2 = az_zd_to_cx_cy_cz(
        azimuth_rad=azimuth2_rad, zenith_rad=zenith2_rad
    )
    return angle_between_cx_cy_cz(cx1, cy1, cz1, cx2, cy2, cz2)


def restore_cz(cx, cy):
    """
    Returns the cz component of a cartesian direction vector assuming it points
    above the x-y plane, i.e. assuming that cz > 0.
    """
    return np.sqrt(1.0 - cx**2 - cy**2)


def arccos_accepting_numeric_tolerance(x, eps=1e-6):
    """
    Just like arccos, but tollerates a wider range of x:
        (-1.0 - eps) < x < (+1.0 + eps)
    before warning and returning nan.

    Parameters
    ----------
    x : float
        Distance.
    eps : float
        Tolerance for x.

    Returns
    -------
    angle : float
    """
    # input dimensionality
    x = np.asarray(x)
    scalar_input = False
    if x.ndim == 0:
        x = x[np.newaxis]  # Makes x 1D
        scalar_input = True

    # work
    assert eps >= 0.0
    mask = np.logical_and(x > 1.0, x < (1.0 + eps))
    x[mask] = 1.0
    mask = np.logical_and(x < -1.0, x > (-1.0 - eps))
    x[mask] = -1.0
    ret = np.arccos(x)

    # output dimensionality
    if scalar_input:
        return np.squeeze(ret)
    return ret
