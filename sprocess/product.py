"""
    Product classes which represent files on disk and processing required
"""

import os
import errno
import shutil
from tempfile import mkdtemp
from gippy.algorithms import Indices
from .scene import scene_open_check


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

    @scene_open_check
    def process(self, method, path=None):
        # if the image is not open, open it first

        tmp_folder = mkdtemp()
        if path:
            if os.path.isdir(path):
                outfile = os.path.join(path + self.product_name(method))
            else:
                outfile = path
        else:
            outfile = os.path.join(tmp_folder + self.product_name(method))

        prods = {method: outfile}
        ndvi_image = Indices(self.geoimg, prods)
        try:
            shutil.rmtree(tmp_folder)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

        name = ndvi_image.BandNames()
        self.geoimg.AddBand(ndvi_image[name[0]])
        self.geoimg.SetBandName(method, self.geoimg.NumBands())
        return self


class NDVI(BaseIndices):
    description = 'Normalized Difference Vegetation Index (NDVI) from TOA reflectance'
    ndvi_enabled = False

    def ndvi(self, path=None):
        return self.process('ndvi', path)


class EVI(BaseIndices):
    description = 'EVI'
    evi_enabled = False

    def evi(self, path=None):
        return self.process('evi', path)
