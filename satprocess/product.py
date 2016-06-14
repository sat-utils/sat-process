"""
    Product classes which represent files on disk and processing required
"""

import os
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
    dependencies = {}

    def __init__(self, scene):
        """ Initialize a product with a Scene, which contains other products """
        # products don't exist on their own, they are owned by a parent Scene
        self.scene = scene
        # start with no GeoImage
        self.geoimg = None

    def open(self, filenames=None, bandnames=None, **kwargs):
        """ Open series of files {bandname: filename} as a product """
        if filenames is None:
            # get the filenames from the scene
            filenames = self.scene.filenames.values()
            bandnames = self.scene.filenames.keys()
        if len(filenames) > 0:
            self.geoimg = GeoImage.open(filenames, bandnames=bandnames, **kwargs)
        return self.geoimg

    def get_dependencies(self):
        geoimgs = []
        for d in self.dependencies:
            geoimg = self.scene[d].process()
            # check required bands present
            if not geoimg.bands_exist(self.dependencies[d]):
                raise SatProcessError('%s requires bands: %s' % (self.name, ' '.join(self.dependencies[d])))
            geoimgs.append(geoimg)
        return geoimgs

    def process(self, filename=None, **kwargs):
        """ Check if already exists or process and return GeoImage """
        self.filename = self.get_filename() if filename is None else filename
        # get and return dependencies
        return self.geoimg

    def get_filename(self):
        """ Return an appropriate output filename for this product """
        return os.path.join(self.scene.outpath, self.scene.basename + '_%s' % self.name)


class DigitalCounts(Product):
    name = 'dc'
    description = 'Digital counts'


class TOA(Product):
    """ Top of the atmosphere reflectance example """
    name = 'toa'
    description = 'Top of the Atmosphere Reflectance'

    dependencies = {'dc': []}

    def process(self, **kwargs):
        """ Get TOA reflectance """
        super(TOA, self).process(**kwargs)
        if self.geoimg is None:
            geoimgs = self.get_dependencies()
            # convert from digital counts to reflectance
            self.geoimg = geoimgs[0]
        return self.geoimg


class NDVI(Product):
    name = 'ndvi'
    description = 'Normalized Difference Vegetation Index (NDVI) from TOA reflectance'

    dependencies = {'toa': ['nir', 'red']}

    def process(self, **kwargs):
        super(NDVI, self).process(**kwargs)
        if self.geoimg is None:
            geoimgs = self.get_dependencies()
            self.geoimg = indices(geoimgs[0], ['ndvi'], filename=self.filename)
        return self.geoimg


class EVI(Product):
    name = 'evi'
    description = 'Enhanced Vegetation Index'

    dependencies = {'toa': ['nir', 'red', 'blue']}

    def process(self, **kwargs):
        super(EVI, self).process(**kwargs)
        if self.geoimg is None:
            geoimgs = self.get_dependencies()
            self.geoimg = indices(geoimgs[0], ['evi'], filename=self.filename)
        return self.geoimg


class Color(Product):
    name = 'color'
    description = 'Byte-scaled color image with 3 chosen bands'

    dependencies = {'toa': []}

    def process(self, bands=['red', 'green', 'blue'], **kwargs):
        """ Color does not retain the geoimg, since it could be different """
        super(Color, self).process(**kwargs)
        # dependent on these bands
        self.dependencies[self.dependencies.keys()[0]] = bands
        geoimgs = self.get_dependencies()
        self.filename = self.filename + ''.join([c[0] for c in bands])
        # should nodata be explicitly set to 0 here?
        return geoimgs[0].select(bands).autoscale(1, 255).save(self.filename, dtype='byte')
