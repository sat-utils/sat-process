#!/usr/bin/env python

from scene import Scene
from product import Product, NDVI


# Landsat specific Products
class DC(Product):
    description = 'Digital counts'

    # bandmap
    _bandmap = {
        'B1': 'coastal',
        'B2': 'blue',
        'B3': 'green',
        'B4': 'red',
        'B5': 'nir',
        'B6': 'swir1',
        'B7': 'swir22',
        'B8': 'pan',
        'B9': 'cirrus',
        # don't bother with longwave right now
        # 'B10': 'lwir1',
        # 'B11': 'lwir2',
        'BQA': 'quality'
    }

    @classmethod
    def pattern(cls):
        """ Regular expression for matching product files """
        return r'^(LC8.*)_(B.*)\.TIF$'

    def process(self, **kwargs):
        geoimg = super(DC, self).process(**kwargs)
        geoimg.SetNoData(0)
        return geoimg


class TOA(Product):
    description = 'Top of the Atmosphere Reflectance'
    dependencies = {'dc': []}

    def process(self, **kwargs):
        """ Create TOA """
        geoimg = super(TOA, self).process(**kwargs)
        # set gain and offset to convert to TOA
        """
        # need day of year, solar zenith, and band irradiance constants
        day = 0
        irrad = 0
        solarzenith = 0
        theta = np.pi * solarzenith / 180.0
        sundist = (1.0 - 0.016728 * np.cos(np.pi * 0.9856 * (float(day) - 4.0) / 180.0))
        for band in geoimg:
            band = band * (1.0 / ((irrad * np.cos(theta)) / (np.pi * sundist * sundist)))
        """
        return geoimg


class Landsat8Scene(Scene):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _products = {
        DC.name(): DC,
        TOA.name(): TOA,
        NDVI.name(): NDVI,
        # 'pansharpen': PanSharpen
    }

