import numpy as np


def _in(x):
    x = np.asarray(x)
    is_scalar = False
    if x.ndim == 0:
        x = x[np.newaxis]  # Makes x 1D
        is_scalar = True
    return is_scalar, x


def _out(is_scalar, x):
    if is_scalar:
        return np.squeeze(x).item()
    else:
        return x
