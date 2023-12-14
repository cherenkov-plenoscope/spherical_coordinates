import spherical_coordinates as sphcors
import numpy as np
import pytest
import warnings


assert_close = np.testing.assert_almost_equal


def test_arccos():
    md_arccos = sphcors.arccos_accepting_numeric_tolerance

    vvv = np.linspace(-1, 1, 1000)
    for v in vvv:
        assert md_arccos(v) == np.arccos(v)
    np.testing.assert_array_equal(md_arccos(v), np.arccos(v))

    lll = -1 - 1.1e-6
    with pytest.warns(RuntimeWarning):
        v = md_arccos(lll, eps=1e-6)
    with pytest.warns(RuntimeWarning):
        v = md_arccos(np.array([lll, 0.0]), eps=1e-6)

    ppp = 1 + 1.1e-6
    with pytest.warns(RuntimeWarning):
        v = md_arccos(ppp, eps=1e-6)
    with pytest.warns(RuntimeWarning):
        v = md_arccos(np.array([ppp, 0.0]), eps=1e-6)

    cccppp = 1 + 0.9e-6
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        v = md_arccos(cccppp, eps=1e-6)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        v = md_arccos(np.array([0.0, cccppp]), eps=1e-6)

    ccclll = -1 - 0.9e-6
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        v = md_arccos(ccclll, eps=1e-6)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        v = md_arccos(np.array([0.0, 0.1, ccclll]), eps=1e-6)


def test_azimuth_range():
    PI = np.pi
    assert_close(0, sphcors.azimuth_range(0))
    assert_close(PI / 2, sphcors.azimuth_range(PI / 2))
    assert_close(PI, sphcors.azimuth_range(PI))
    assert_close(-PI + 1e-3, sphcors.azimuth_range(PI + 1e-3))
    assert_close(-PI / 2, sphcors.azimuth_range(-PI / 2))
    assert_close(PI, sphcors.azimuth_range(-PI))


def test_azimuth_range_array():
    PI = np.pi
    arr = sphcors.azimuth_range(
        azimuth_rad=np.array([0.0, PI / 2, PI, PI + 1e-2, -PI])
    )
    assert_close(arr[0], 0.0)
    assert_close(arr[1], PI / 2)
    assert_close(arr[2], PI)
    assert_close(arr[3], -PI + 1e-2)
    assert_close(arr[4], PI)


def test_angles_scalars_hemisphere():
    for az in np.linspace(np.deg2rad(-380), np.deg2rad(380), 25):
        for zd in np.linspace(np.deg2rad(0), np.deg2rad(89), 25):
            cx, cy = sphcors.az_zd_to_cx_cy(azimuth_rad=az, zenith_rad=zd)
            az_back, zd_back = sphcors.cx_cy_to_az_zd(cx=cx, cy=cy)
            delta = sphcors.angle_between_az_zd(
                azimuth1_rad=az,
                zenith1_rad=zd,
                azimuth2_rad=az_back,
                zenith2_rad=zd_back,
            )
            assert delta < np.deg2rad(1e-3)


def test_angles_scalars_fullsphere():
    for az in np.linspace(np.deg2rad(-380), np.deg2rad(380), 25):
        for zd in np.linspace(np.deg2rad(0), np.deg2rad(180), 50):
            cx, cy, cz = sphcors.az_zd_to_cx_cy_cz(
                azimuth_rad=az, zenith_rad=zd
            )
            az_back, zd_back = sphcors.cx_cy_cz_to_az_zd(cx=cx, cy=cy, cz=cz)
            delta = sphcors.angle_between_az_zd(
                azimuth1_rad=az,
                zenith1_rad=zd,
                azimuth2_rad=az_back,
                zenith2_rad=zd_back,
            )
            assert delta < np.deg2rad(1e-3)


def test_angles_arrays_hemisphere():
    num = 625
    az = np.linspace(np.deg2rad(-380), np.deg2rad(380), num)
    zd = np.linspace(np.deg2rad(0), np.deg2rad(89), num)

    cx, cy = sphcors.az_zd_to_cx_cy(azimuth_rad=az, zenith_rad=zd)
    assert len(cx) == len(cy)
    assert len(cx) == num

    az_back, zd_back = sphcors.cx_cy_to_az_zd(cx=cx, cy=cy)
    assert len(az_back) == len(zd_back)
    assert len(az_back) == num

    delta = sphcors.angle_between_az_zd(
        azimuth1_rad=az,
        zenith1_rad=zd,
        azimuth2_rad=az_back,
        zenith2_rad=zd_back,
    )
    assert len(delta) == num
    assert np.all(delta < 1e-3)


def test_angles_arrays_fullsphere():
    num = 625
    az = np.linspace(np.deg2rad(-380), np.deg2rad(380), num)
    zd = np.linspace(np.deg2rad(0), np.deg2rad(180), num)

    cx, cy, cz = sphcors.az_zd_to_cx_cy_cz(azimuth_rad=az, zenith_rad=zd)
    assert len(cx) == len(cy)
    assert len(cx) == len(cz)
    assert len(cx) == num

    az_back, zd_back = sphcors.cx_cy_cz_to_az_zd(cx=cx, cy=cy, cz=cz)
    assert len(az_back) == len(zd_back)
    assert len(az_back) == num

    delta = sphcors.angle_between_az_zd(
        azimuth1_rad=az,
        zenith1_rad=zd,
        azimuth2_rad=az_back,
        zenith2_rad=zd_back,
    )
    assert len(delta) == num
    assert np.all(delta < 1e-3)
