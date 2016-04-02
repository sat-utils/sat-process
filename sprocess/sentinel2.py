#!/usr/bin/env python

from scene import Scene
from product import Product, NDVI


class TOA(Product):
    description = 'Top of the Atmosphere Reflectance'

    _bandmap = {
        'B01': 'coastal',
        'B02': 'blue',
        'B03': 'green',
        'B04': 'red',
        'B08': 'nir',
        'B10': 'cirrus',
        'B11': 'swir1',
        'B12': 'swir2'
    }

    @classmethod
    def pattern(cls):
        """ Regular expression for matching product files """
        return r'(.*)_(B.*)\.jp2$'

    def process(self, **kwargs):
        """ Create TOA """
        geoimg = super(TOA, self).process(**kwargs)
        geoimg.SetNoData(0)
        geoimg.SetGain(0.0001)
        return geoimg


class Sentinel2Scene(Scene):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _products = {
        # original products
        TOA.name(): TOA,
        # dervied products
        NDVI.name(): NDVI
    }
