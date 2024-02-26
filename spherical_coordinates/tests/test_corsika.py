import spherical_coordinates as sphcors
import numpy as np

assert_close = np.testing.assert_almost_equal


def test_corsika_theta_phi():
    zd = np.linspace(-32, 24, 13337)
    theta = sphcors.corsika.zd_to_theta(zenith_rad=zd)
    assert_close(theta, zd)

    zd_back = sphcors.corsika.theta_to_zd(theta_rad=theta)
    assert_close(zd_back, zd)

    az = np.linspace(-32, 24, 13337)
    phi = sphcors.corsika.az_to_phi(azimuth_rad=az)
    assert_close(phi + np.pi, az)

    az_back = sphcors.corsika.phi_to_az(phi_rad=phi)
    assert_close(
        sphcors.azimuth_range(azimuth_rad=az_back),
        sphcors.azimuth_range(azimuth_rad=az),
    )


def test_corsika_minimal_example():
    prng = np.random.Generator(np.random.PCG64(75600))

    for case in range(1000):
        # draw pointing of cosmic primary particle
        az = prng.uniform(low=-100, high=100)
        zd = prng.uniform(low=0.0, high=np.deg2rad(60))

        cx, cy, cz = sphcors.az_zd_to_cx_cy_cz(azimuth_rad=az, zenith_rad=zd)

        # tell corsika the momentum of the particle in phi and theta
        phi = sphcors.corsika.az_to_phi(azimuth_rad=az)
        theta = sphcors.corsika.zd_to_theta(zenith_rad=zd)

        # corsika simulates a shower...
        # this is what I think is happening inside of CORSIKA
        #
        # See corsikacompilefile.f lines between 0 and 1e6.
        #
        # line 6375
        # ---------
        # PRMPAR(2) = COS( THETAP )
        # PRMPAR(3) = SIN( THETAP ) * COS( PHIP )
        # PRMPAR(4) = SIN( THETAP ) * SIN( PHIP )
        #
        # C  CURPAR(2)   = COSTHE, DIRECTION COSINE Z-DIRECTION
        # C  CURPAR(3)   = PHIX,   DIRECTION COSINE X-DIRECTION
        # C  CURPAR(4)   = PHIY,   DIRECTION COSINE Y-DIRECTION
        #
        # line 161717 SUBROUTINE CERENK
        # ----------- -----------------
        # the mean direction of the cherenkov light
        #
        # C   UMEAN  = DIRECTION COSINE TO X AXIS (STEP AVERAGE)
        # C   VMEAN  = DIRECTION COSINE TO Y AXIS (STEP AVERAGE)
        # C   WMEAN  = DIRECTION COSINE TO -Z AXIS (STEP AVERAGE)
        #
        # in between are a gazillion minus signs and different frames used
        # by e.g. EGS.
        # Most terrefying are minus signs on V (y axis) in the call of CERENK:
        #   VMEAN = -VMEAN  <--- WTF????
        #
        # It is hopeless to understand what happens.
        # But I think this is what happens:

        cherenkov_momentum_x = np.sin(theta) * np.cos(phi)
        cherenkov_momentum_y = np.sin(theta) * np.sin(phi)
        cherenkov_momentum_z = (-1.0) * np.cos(theta)

        # finally CORSIKA returns cherenkov light with ux and vy in its output.
        ux = cherenkov_momentum_x
        vy = cherenkov_momentum_y

        # IF CORSIKA works as I think it does, this should hold:
        assert_close(cx, sphcors.corsika.ux_to_cx(ux=ux))
        assert_close(cy, sphcors.corsika.vy_to_cy(vy=vy))
