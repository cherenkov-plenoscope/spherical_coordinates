import spherical_coordinates as sphcors
import numpy as np
import pytest
import warnings


assert_close = np.testing.assert_almost_equal


def test_dimensionality_float():
    is_scalar, x_work = sphcors._dimensionality_in(float(9))
    assert is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors._dimensionality_out(is_scalar, x=x_work)
    assert isinstance(x_out, float)


def test_dimensionality_list():
    is_scalar, x_work = sphcors._dimensionality_in([1, 2, 3, 4])
    assert not is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors._dimensionality_out(is_scalar, x=x_work)
    assert isinstance(x_out, np.ndarray)


def test_dimensionality_array():
    is_scalar, x_work = sphcors._dimensionality_in(np.array([1, 2, 3, 4]))
    assert not is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors._dimensionality_out(is_scalar, x=x_work)
    assert isinstance(x_out, np.ndarray)


def test_dimensionality_array_item():
    arr = np.array([1, 2, 3, 4])
    is_scalar, x_work = sphcors._dimensionality_in(arr[2])
    assert is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors._dimensionality_out(is_scalar, x=x_work)
    assert isinstance(x_out, float)


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


def test_angle_between_xyz():
    N = np.pi / 2
    R = np.pi
    ar = np.array

    x = ar([1, 0, 0])
    y = ar([0, 1, 0])
    z = ar([0, 0, 1])
    aaa = [x, x, x, x]
    bbb = [x, y, z, -x]
    ddd = [0, N, N, R]

    delta = sphcors.angle_between_xyz(a=[0, 0, 1], b=[0, 0, 1])
    assert delta == 0.0

    delta = sphcors.angle_between_xyz(a=aaa, b=bbb)
    np.testing.assert_array_almost_equal(delta, ddd)
