#####################
Spherical Coordinates
#####################
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|

A python package to transform the representations of pointings. It adopts the
naming and definitions of KIT's CORSIKA_.
The transformations support both scalar and array-like in- and outputs, as in
numpy_. Only free floating functions. No custom classes or structures.


|img_frame|


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

In equations within CORSIKA's documents, the azimuth angle is represented
by greek letter ``Phi`` and the zenith angle is represented by
greek letter ``Theta``. Here, we use CORSIKA's explicit names 'azimuth'
and 'zenith' as they are used in the text body of e.g. CORSIKA's manual.

.. code:: python

    import spherical_coordinates

    cx, cy, cz = spherical_coordinates.az_zd_to_cx_cy_cz(
        azimuth_rad=0.2,
        zenith_rad=0.3,
    )
    print(cx, cy, cz)
    0.28962947762551555 0.058710801693826566 0.955336489125606

    az, zd = spherical_coordinates.cx_cy_cz_to_az_zd(cx=cx, cy=cy, cz=cz)
    print(az, zd)
    0.20000000000000015 0.30000000000000016


Hemisphere in positive Z
========================

Often, CORSIKA assumes that all directions point above the x-y plane in what
case it neglects the Z-component. For example this is the case in the output
files for particles or Cherenkov photons where only (``cx`` and ``cy``) are
given. To not always restore the missing ``cz`` component manually, there
are transformations for this limited, but unfortunately common case. I suspect
CORSIKA omitted the ``cz`` to reduce storage space. For new projects, I would
not recommand this.


.. code:: python

    import spherical_coordinates

    cx, cy = spherical_coordinates.az_zd_to_cx_cy(
        azimuth_rad=0.2,
        zenith_rad=0.3,
    )
    print(cx, cy, cz)
    0.28962947762551555 0.058710801693826566

    az, zd = spherical_coordinates.cx_cy_to_az_zd(cx=cx, cy=cy)
    print(az, zd)
    0.20000000000000015 0.30000000000000016


However, for pointings below the x-y plane this will fail:

.. code:: python

    import spherical_coordinates

    zenith_below_xy_plane_rad = 2.0
    cx, cy = spherical_coordinates.az_zd_to_cx_cy(
        azimuth_rad=0.2,
        zenith_rad=zenith_below_xy_plane_rad,
    )
    az, zd = spherical_coordinates.cx_cy_to_az_zd(cx=cx, cy=cy)
    print(zd)
    1.1415926535897933
    # zd is now the projection into the upper hemisphere


To restore ``cz`` there is:

.. code:: python

    import spherical_coordinates

    cz = spherical_coordinates.restore_cz(cx=0.1, cy=0.2)
    print(cz)


what assumes the lengths is 1.0:

.. math::

    cz = sqrt{1.0 - cx * cx - cy * cy}


**************
Angles Between
**************

Quickly estimate the angle between two pointings.

.. code:: python

    import spherical_coordinates

    delta = spherical_coordinates.angle_between_cx_cy_cz(
        cx1=0.5, cy1=0.5, cz1=0.7071, cx2=0.7071, cy2=0.0, cz2=0.7071
    )
    print(delta*180/3.14159, "DEG")
    31.399818557245204 DEG

    delta = spherical_coordinates.angle_between_cx_cy(
        cx1=0.5, cy1=0.5, cx2=0.7071, cy2=0.0
    )
    print(delta*180/3.14159, "DEG")
    31.399818557245204 DEG

    delta = spherical_coordinates.angle_between_az_zd(
        azimuth1_rad=1.2, zenith1_rad=0.2, azimuth2_rad=-0.5, zenith2_rad=0.7
    )
    print(delta*180/3.14159, "DEG")
    42.852624700439804 DEG


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

.. |img_frame| image:: https://github.com/cherenkov-plenoscope/spherical_coordinates/blob/main/readme/frame.png?raw=True
