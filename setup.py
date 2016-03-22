#!/usr/bin/env python


from setuptools import setup, find_packages
import imp


__version__ = imp.load_source('multispectral.version', 'multispectral/version.py').__version__


setup(
    name='sat-multispectral',
    version=__version__,
    description='Multispectral processing on geospatial raster data',
    packages=find_packages(),
    install_requires=['gippy'],
)
