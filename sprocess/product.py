"""
    Product classes which represent files on disk and processing required
"""

import numpy as np
from gippy.algorithms import indices
from utils import rescale_intensity
from errors import SatProcessError


class Product(object):
    """ A Product is some input (either files, or another series of Products)
        and some processing performed on that input. """

    description = 'Product Base Class'
    name = 'product'

    # dependencies in the form {product: [bands]}
    dependencies = {}

    # map of original band names to common bandnames
    _bandmap = {}

    def product_name(self, method):
        return method + '_' + self.basename()


class BaseIndices(Product):
    description = 'Base class for Indices'
    dependencies = []

    def process(self, method, path=None):
        args = [self, [method]]

        if path:
            args.append(path)

        new_image = indices(*args)
        return self.__class__(new_image)


class ColorCorrection(BaseIndices):

    def snow_cloud_coverage(self):

        self.has_bands(['quality'])

        quality = self['quality'].read()
        cloud_high_conf = int('1100000000000000', 2)
        snow_high_conf = int('0000110000000000', 2)
        fill_pixels = int('0000000000000001', 2)
        cloud_mask = np.bitwise_and(quality, cloud_high_conf) == cloud_high_conf
        snow_mask = np.bitwise_and(quality, snow_high_conf) == snow_high_conf
        fill_mask = np.bitwise_and(quality, fill_pixels) == fill_pixels

        perc = np.true_divide(np.sum(cloud_mask | snow_mask),
                              quality.size - np.sum(fill_mask)) * 100.0

        return perc

    def color_correction(self, bands=range(0, 3), snow_cloud_coverage=0, auto_cloud=True):

        if auto_cloud:
            snow_cloud_coverage = self.snow_cloud_coverage()

        if not isinstance(bands, list):
            raise SatProcessError('bands must be a python list')

        print('color correcting')

        i = 0
        for i in bands:
            band = self[i]
            band_np = band.read()
            p_low, cloud_cut_low = np.percentile(band_np[np.logical_and(band_np > 0, band_np < 65535)],
                                                 (0, 100 - (snow_cloud_coverage * 3 / 4)))
            temp = np.zeros(np.shape(band_np), dtype=np.uint16)
            cloud_divide = 65000 - snow_cloud_coverage * 100
            mask = np.logical_and(band_np < cloud_cut_low, band_np > 0)
            temp[mask] = rescale_intensity(band_np[mask],
                                           in_range=(p_low, cloud_cut_low),
                                           out_range=(256, cloud_divide))
            temp[band_np >= cloud_cut_low] = rescale_intensity(band_np[band_np >= cloud_cut_low],
                                                               out_range=(cloud_divide, 65535))
            self[i].write(temp)
            i += 1

        return self


class TrueColor(BaseIndices):

    def true_color(self, path=None):
        required_bands = ['red', 'green', 'blue']

        # make sure red, green, blue is present
        self.has_bands(required_bands)
        rgb = self.select(required_bands)

        if path:
            rgb.save(path)
        return rgb


class NDVI(BaseIndices):
    description = 'Normalized Difference Vegetation Index (NDVI) from TOA reflectance'
    ndvi_enabled = False

    def ndvi(self, path=None):
        # Make sure band red and nir are present
        if 'nir' not in self.bands:
            raise SatProcessError('nir band is not provided')

        if 'red' not in self.bands:
            raise SatProcessError('red band is not provided')

        return self.process('ndvi', path)


class EVI(BaseIndices):
    description = 'EVI'
    evi_enabled = False

    def evi(self, path=None):
        return self.process('evi', path)
