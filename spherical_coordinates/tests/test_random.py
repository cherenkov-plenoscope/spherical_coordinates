import spherical_coordinates as sc
import numpy as np


def example_cone_orientations():
    return [
        {"azimuth_rad": 0.0, "zenith_rad": 0.0},
        {"azimuth_rad": 1.0, "zenith_rad": 0.0},
        {"azimuth_rad": 2.0, "zenith_rad": 1.0},
        {"azimuth_rad": -2.0, "zenith_rad": 2.0},
        {"azimuth_rad": np.pi, "zenith_rad": np.pi},
    ]


def test_size():
    prng = np.random.Generator(np.random.PCG64(132))

    size_shapes = {
        None: (),
        0: (0,),
        1: (1,),
        100: (100,),
    }

    for size in size_shapes:
        az, zd = sc.random.uniform_az_zd_in_cone(
            prng=prng,
            azimuth_rad=0.0,
            zenith_rad=0.0,
            min_half_angle_rad=0.0,
            max_half_angle_rad=1.0,
            size=size,
        )

        assert np.shape(az) == size_shapes[size]
        assert np.shape(zd) == size_shapes[size]


def test_output_distribution_on_full_sphere():
    prng = np.random.Generator(np.random.PCG64(132))

    for cone in example_cone_orientations():
        az, zd = sc.random.uniform_az_zd_in_cone(
            prng=prng,
            azimuth_rad=cone["azimuth_rad"],
            zenith_rad=cone["zenith_rad"],
            min_half_angle_rad=0.0,
            max_half_angle_rad=np.pi,
            size=1000 * 1000,
        )

        eps = np.deg2rad(1)
        NUM_AZIMUTH_STEPS = 12
        for i in range(NUM_AZIMUTH_STEPS):
            q = i / NUM_AZIMUTH_STEPS
            q_az = np.quantile(az, q=q)
            expected_q_az = -np.pi + q * (2.0 * np.pi)
            assert expected_q_az - eps < q_az < expected_q_az + eps

        z = np.cos(zd)
        eps_z = 1e-2
        NUM_Z_SEPS = 12
        for i, expected_z in enumerate(
            np.linspace(-1, 1, NUM_Z_SEPS, endpoint=False)
        ):
            q = i / NUM_Z_SEPS
            q_z = np.quantile(z, q=q)
            assert expected_z - eps_z < q_z < expected_z + eps_z


def test_cone():
    prng = np.random.Generator(np.random.PCG64(133))

    eps_rad = np.deg2rad(1)
    for cone in example_cone_orientations():
        az, zd = sc.random.uniform_az_zd_in_cone(
            prng=prng,
            azimuth_rad=cone["azimuth_rad"],
            zenith_rad=cone["zenith_rad"],
            min_half_angle_rad=0.0,
            max_half_angle_rad=np.deg2rad(1.0),
            size=1000,
        )

        cx, cy, cz = sc.az_zd_to_cx_cy_cz(azimuth_rad=az, zenith_rad=zd)

        mcx = np.mean(cx)
        mcy = np.mean(cy)
        mcz = np.mean(cz)

        norm = np.sqrt(mcx**2 + mcy**2 + mcz**2)
        mcx /= norm
        mcy /= norm
        mcz /= norm

        ecx, ecy, ecz = sc.az_zd_to_cx_cy_cz(
            azimuth_rad=cone["azimuth_rad"], zenith_rad=cone["zenith_rad"]
        )

        delta_rad = sc.angle_between_cx_cy_cz(
            cx1=mcx,
            cy1=mcy,
            cz1=mcz,
            cx2=ecx,
            cy2=ecy,
            cz2=ecz,
        )

        assert delta_rad < eps_rad
