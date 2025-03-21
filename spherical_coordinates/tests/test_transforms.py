import spherical_coordinates as sphcors
import numpy as np
import pytest
import warnings


assert_close = np.testing.assert_almost_equal


def test_dimensionality_float():
    is_scalar, x_work = sphcors.dimensionality._in(float(9))
    assert is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors.dimensionality._out(is_scalar, x=x_work)
    assert isinstance(x_out, float)


def test_dimensionality_list():
    is_scalar, x_work = sphcors.dimensionality._in([1, 2, 3, 4])
    assert not is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors.dimensionality._out(is_scalar, x=x_work)
    assert isinstance(x_out, np.ndarray)


def test_dimensionality_array():
    is_scalar, x_work = sphcors.dimensionality._in(np.array([1, 2, 3, 4]))
    assert not is_scalar
    assert isinstance(x_work, np.ndarray)
    x_out = sphcors.dimensionality._out(is_scalar, x=x_work)
    assert isinstance(x_out, np.ndarray)


def test_dimensionality_array_item():
    cases = {
        "float": {"arr": np.array([1.0, 2.0, 3.0, 4.0]), "dtype": float},
        "int": {"arr": np.array([1, 2, 3, 4]), "dtype": int},
    }
    for key in cases:
        arr = cases[key]["arr"]
        expected_dtype = cases[key]["dtype"]
        is_scalar, x_work = sphcors.dimensionality._in(arr[2])
        assert is_scalar
        assert isinstance(x_work, np.ndarray)
        x_out = sphcors.dimensionality._out(is_scalar, x=x_work)
        assert isinstance(x_out, expected_dtype)


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


def test_restore_cz_numerics():
    cz = sphcors.restore_cz(cx=0.0, cy=0.0, eps=0.0)
    assert cz == 1.0

    cz = sphcors.restore_cz(cx=1.0, cy=0.0, eps=0.0)
    assert cz == 0.0

    cz = sphcors.restore_cz(cx=0.0, cy=1.0, eps=0.0)
    assert cz == 0.0

    with pytest.warns(RuntimeWarning):
        cz = sphcors.restore_cz(1.0, 1e-6, eps=0.0)
    cz = sphcors.restore_cz(1.0, 1e-6, eps=1e-6)

    with pytest.warns(RuntimeWarning):
        cz = sphcors.restore_cz(1e-6, 1.0, eps=0.0)
    cz = sphcors.restore_cz(1e-6, 1.0, eps=1e-6)

    with pytest.warns(RuntimeWarning):
        cz = sphcors.restore_cz(1.0 + 1e-6, 0.0, eps=0.0)

    cz = sphcors.restore_cz(1.0 + 0.2e-6, 0.0, eps=1e-6)


def test_restore_cz():
    prng = np.random.Generator(np.random.PCG64(seed=44))
    NUM = 10_000

    cx = prng.uniform(low=-1.0, high=1.0, size=NUM)
    cy = prng.uniform(low=-1.0, high=1.0, size=NUM)
    cz = prng.uniform(low=0.0, high=1.0, size=NUM)

    norms = np.linalg.norm(np.c_[cx, cy, cz], axis=1)
    cx /= norms
    cy /= norms
    cz /= norms

    # array like
    cz_restore = sphcors.restore_cz(cx=cx, cy=cy, eps=1e-6)
    np.testing.assert_array_almost_equal(desired=cz, actual=cz_restore)

    # scalar like
    for i in range(NUM):
        cz_restore = sphcors.restore_cz(cx=cx[i], cy=cy[i], eps=1e-6)
        np.testing.assert_almost_equal(desired=cz[i], actual=cz_restore)


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


def test_different_dimensionality():
    lin05 = np.linspace(0.0, 1.0, 5)

    # both scalars
    angles = sphcors.angle_between_az_zd(
        azimuth1_rad=0.0,
        zenith1_rad=0.0,
        azimuth2_rad=0.0,
        zenith2_rad=0.0,
    )
    assert isinstance(angles, float)
    np.testing.assert_almost_equal(angles, 0.0)

    # both vectors
    ANGLES = sphcors.angle_between_az_zd(
        azimuth1_rad=lin05,
        zenith1_rad=lin05,
        azimuth2_rad=-lin05,
        zenith2_rad=lin05,
    )
    assert isinstance(ANGLES, np.ndarray)
    assert ANGLES.shape[0] == 5
    assert len(ANGLES.shape) == 1

    # first is scalar
    angles = sphcors.angle_between_az_zd(
        azimuth1_rad=0,
        zenith1_rad=0,
        azimuth2_rad=-lin05,
        zenith2_rad=lin05,
    )
    assert isinstance(angles, np.ndarray)
    assert angles.shape[0] == 5
    assert len(angles.shape) == 1
    np.testing.assert_array_almost_equal(angles, lin05)

    # second is scalar
    angles = sphcors.angle_between_az_zd(
        azimuth1_rad=lin05,
        zenith1_rad=lin05,
        azimuth2_rad=-1,
        zenith2_rad=1,
    )
    assert isinstance(angles, np.ndarray)
    assert angles.shape[0] == 5
    assert len(angles.shape) == 1
