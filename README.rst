sat-process
+++++++++++

.. image:: https://travis-ci.org/sat-utils/sat-process.svg?branch=develop
    :target: https://travis-ci.org/sat-utils/sat-process

This is a Python library for processing toolkit for Open Raster Data. This is library can be used for creating data specific processing libraries and command line utilities.

Process remote sensing images with this library using two main steps:

1. Assemble all required bands and metadata into a Scene object

2. Create process object with the Scene object and desired functions

Standard Band Names
===================

Band names are used instead of band numbers, which are unique to each sensor. The average ranges for spectral bandpasses are given in the table below, along with the band numbers for several sensors.

+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Band Name | Band Ranges | Landsat 5 | Landsat 7 | Landsat 8 | Sentinel 2 | MODIS |
+===========+=============+===========+===========+===========+============+=======+
| Coastal   | 0.40 - 0.45 |           |           | 1         | 1          |       |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Blue      | 0.45 - 0.5  | 1         | 1         | 2         | 2          | 3     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Green     | 0.5 - 0.6   | 2         | 2         | 3         | 3          | 4     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Red       | 0.6 - 0.7   | 3         | 3         | 4         | 4          | 1     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Pan       | 0.5 - 0.7   |           | 8         | 8         |            |       |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| NIR       | 0.77 - 1.00 | 4         | 4         | 5         | 8          | 2     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| Cirrus    | 1.35 - 1.40 |           |           | 9         | 10         | 26    |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| SWIR1     | 1.55 - 1.75 | 5         | 5         | 6         | 11         | 6     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| SWIR2     | 2.1 - 2.3   | 7         | 7         | 7         | 12         | 7     |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| LWIR      | 10.5 - 12.5 | 6         | 8         |           |            |       |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| LWIR1     | 10.5 - 11.5 |           |           | 10        |            | 31    |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
| LWIR2     | 11.5 - 12.5 |           |           | 11        |            | 32    |
+-----------+-------------+-----------+-----------+-----------+------------+-------+
