import numpy as np
from . import base


def draw_cx_cy_cz(prng, size=None):
    cx = prng.uniform(low=-1, high=1, size=size)
    cy = prng.uniform(low=-1, high=1, size=size)
    cz = prng.uniform(low=1e-3, high=1, size=size)
    cxcycz = np.c_[cx, cy, cz]
    cxcycz_norm = np.linalg.norm(cxcycz, axis=1)
    for m in range(len(cxcycz_norm)):
        cxcycz[m, :] /= cxcycz_norm[m]

    if size is None:
        return (cxcycz[0, 0], cxcycz[0, 1], cxcycz[0, 2])
    else:
        return (cxcycz[:, 0], cxcycz[:, 1], cxcycz[:, 2])


def draw_cx_cy(prng, size=None):
    cx, cy, cz = draw_cx_cy_cz(prng=prng, size=size)
    return cx, cy


def draw_az_zd(prng, size=None):
    cx, cy, cz = draw_cx_cy_cz(prng=prng, size=size)
    return base.cx_cy_cz_to_az_zd(cx=cx, cy=cy, cz=cz)
