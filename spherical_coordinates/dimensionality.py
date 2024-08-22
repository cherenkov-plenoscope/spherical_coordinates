import numpy as np


def _in(x):
    """
    Allows to compute input 'x' always as if it is array like
    while the result of a computation can be returned with the same
    dimensionality as the dimensionality of the input 'x'.
    To be used in combination with _out() inside a function.

    Parameters
    ----------
    x : array or scalar like

    Returns
    -------
    (is_scalar, x) : tuple(bool, array like)
        The bool 'is_scalar' is for bookkeeping. The output 'x' is array like
        and has the same content as 'x'.
    """

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
