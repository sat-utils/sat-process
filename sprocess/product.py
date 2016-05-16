"""
    Product classes which represent files on disk and processing required
"""

from gippy.algorithms import indices
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


class TrueColor(BaseIndices):

    def true_color(self, path=None, dtype='byte'):
        required_bands = ['red', 'green', 'blue']
        args = [path]
        kwargs = {}

        # make sure red, green, blue is present
        self.has_bands(required_bands)
        rgb = self.select(required_bands)

        if dtype:
            kwargs['dtype'] = dtype

        if dtype in ['uint8', 'byte']:
            rgb = rgb.autoscale(1, 255)

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
