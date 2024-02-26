from . import dimensionality
import numpy as np


def az_to_phi(azimuth_rad):
    return azimuth_rad - np.pi


def phi_to_az(phi_rad):
    return phi_rad + np.pi


def zd_to_theta(zenith_rad):
    return zenith_rad


def theta_to_zd(theta_rad):
    return theta_rad


def phi_theta_to_az_zd(phi_rad, theta_rad):
    return phi_to_az(phi_rad=phi_rad), theta_to_zd(theta_rad=theta_rad)


def az_zd_to_phi_theta(azimuth_rad, zenith_rad):
    return (
        az_to_phi(azimuth_rad=azimuth_rad),
        zd_to_theta(zenith_rad=zenith_rad),
    )


def ux_to_cx(ux):
    return -ux


def vy_to_cy(vy):
    return -vy


def wz_to_cz(wz):
    return -wz


def cx_to_ux(cx):
    return -cx


def cy_to_vy(cy):
    return -cy


def cz_to_wz(cz):
    return -cz
