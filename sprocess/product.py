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

    def color_correction(self, snow_cloud_coverage=0):

        print('color correcting')
        print(self)
        if self.band_numbers > 3:
            raise SatProcessError('Color Correction can only be applied on three bands')

        i = 0
        for band in self:
            print(i)
            band_np = band.read()
            p_low, cloud_cut_low = np.percentile(band_np[np.logical_and(band_np > 0, band_np < 65535)],
                                                 (0, (snow_cloud_coverage * 3 / 4)))
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

    def true_color(self, path=None, dtype='byte'):
        print(self)
        required_bands = ['red', 'green', 'blue']
        args = [path]
        kwargs = {}

        # make sure red, green, blue is present
        self.has_bands(required_bands)
        rgb = self.select(required_bands)

        if dtype:
            kwargs['dtype'] = dtype

        if dtype in ['uint8', 'byte']:
            self = rgb.autoscale(1, 255)

        if path:
            rgb.save(*args, **kwargs)
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
