"""
    Product classes which represent files on disk and processing required
"""

import os
import re
from gippy import GeoImage
from gippy.algorithms import indices
from errors import SatProcessError


class Product(object):
    """ A Product is some input (either files, or another series of Products)
        and some processing performed on that input. Products are used as mixins
        along with a gippy.GeoImage """

    name = 'product'
    description = 'Product Base Class'

    # dependencies in the form {product: [bands]}
    dependencies = []

    _bandmap = {}

    """ Regular expression for matching product files with 2 groups: basename and band """
    _pattern = r'(.*)_(.*)\..*'

    def __init__(self, scene):
        """ Initialize a product with a Scene, which contains other products """
        # products don't exist on their own, they are owned by a parent Scene
        self.scene = scene
        # start with no GeoImage
        self.geoimg = None

    def open(self, filenames, **kwargs):
        """ Open series of files as a product """
        if len(filenames) > 0 and filenames is not None:
            self.geoimg = GeoImage.open(filenames, **kwargs)
        return self.geoimg

    def process(self, filename=None, **kwargs):
        """ Check if already exists or process and return GeoImage """
        self.filename = self.get_filename() if filename is None else filename
        # geoimg will be None if not already processed - child should do processing
        return self.geoimg

    def get_filename(self):
        """ Return an appropriate output filename for this product """
        return os.path.join(self.scene.outpath, self.scene.basename + '_%s' % self.name)

    def check_bands(self, geoimg):
        """ Check if all bands required for product are in this geoimg or throw error """
        if not geoimg.bands_exist(self.dependencies):
            raise SatProcessError('%s requires bands: %s' % (self.name, ' '.join(self.dependencies)))

    @classmethod
    def parse_filename(cls, filename):
        """ Split out basename and bandname (remapped if _bandmap) """
        m = re.match(cls._pattern, os.path.basename(filename))
        basename = m.group(1)
        bandname = cls._bandmap.get(m.group(2), m.group(2))
        return basename, bandname


class DigitalCounts(Product):
    name = 'dc'
    description = 'Digital counts'


class TOA(Product):
    """ Top of the atmosphere reflectance example """
    name = 'toa'
    description = 'Top of the Atmosphere Reflectance'

    def process(self, **kwargs):
        """ Get TOA reflectance """
        dc = self.scene.dc()
        # convert from digital counts to reflectance
        return dc


class NDVI(Product):
    name = 'ndvi'
    description = 'Normalized Difference Vegetation Index (NDVI) from TOA reflectance'

    dependencies = ['nir', 'red']

    def process(self, **kwargs):
        geoimg = self.scene.toa()
        self.check_bands(geoimg)
        return indices(geoimg, ['ndvi'])


class EVI(Product):
    name = 'evi'
    description = 'Enhanced Vegetation Index'

    dependencies = ['nir', 'red', 'blue']

    def process(self, **kwargs):
        geoimg = self.scene.toa()
        self.check_bands(geoimg)
        return indices(geoimg, ['evi'])


class Color(Product):
    name = 'color'
    description = 'Byte-scaled color image with 3 chosen bands'

    def process(self, bands=['red', 'green', 'blue'], **kwargs):
        geoimg = super(Color, self).process(**kwargs)
        geoimg = geoimg if geoimg is not None else self.scene.toa()
        # TODO - need different filenames based on colors used!!!
        self.filename = self.filename + ''.join([c[0] for c in bands])
        self.dependencies = bands
        self.check_bands(geoimg)
        # should nodata be explicitly set to 0 here?
        geoimg = geoimg.select(bands).autoscale(1, 255).save(self.filename, dtype='byte')
        return geoimg
