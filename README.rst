#####################
Spherical Coordinates
#####################
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|

A python package to transform the representations of pointings. It adopts the
naming and definitions of KIT's CORSIKA_.
The transformations support both scalar and array-like in- and outputs, as in
numpy_. Only free floating functions. No custom classes or structures.


*******
Install
*******

.. code:: bash

    pip install spherical_coordinates


***************
Transformations
***************

CORSIKA uses mainly two representations for directions in three dimensional
space. First, the azimuth-zenith representation, and second cartesian
direction vectors of length 1.

The azimuth-zenith representation uses two floats
(``azimuth_rad`` and ``zenith_rad``).
The cartesian vector uses three floats (``cx``, ``cy``, and ``cz``).


.. code:: python

    import spherical_coordinates

    cx, cy, cz = spherical_coordinates.az_zd_to_cx_cy_cz(
        azimuth_rad=0.2,
        zenith_rad=0.3,
    )


*************
Azimuth Range
*************

From my experience, some parts in CORSIKA expect the azimuth angle to be in the
so called 'least absolute residue'. This is:


.. math::

    - PI < azimuth_rad <= +PI

For this ``spherical_coordinates`` has a range limiter:

.. code:: python

    import spherical_coordinates

    az = spherical_coordinates.azimuth_range(azimuth_rad=123.4)
    print(az*180/3.1415, "DEG")

    -129.7046334064967 DEG


.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/spherical_coordinates/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/spherical_coordinates/actions/workflows/test.yml

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/spherical_coordinates
    :target: https://pypi.org/project/spherical_coordinates

.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |BlackPackStyle| image:: https://img.shields.io/badge/pack%20style-black-000000.svg
    :target: https://github.com/cherenkov-plenoscope/black_pack

.. |MITLicenseBadge| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. _CORSIKA: https://www.iap.kit.edu/corsika/index.php

.. _numpy: https://numpy.org/
