import os
import re
import satprocess.product as p
from errors import SatProcessError


class Scene(object):
    """ A scene is a collection of products (which could be multiple bands) yet
        covers the same (approximate) spatial region and timestamp """

    # available products - override in children
    _available_products = {
        p.DigitalCounts.name: p.DigitalCounts,
        p.TOA.name: p.TOA,
        p.NDVI.name: p.NDVI,
        p.EVI.name: p.EVI,
        p.Color.name: p.Color,
    }

    # Regular expression for matching product files with 2 groups: baename, band
    # default pattern of form basename_bandname.extension
    _pattern = r'(.*)_(.*)\.(TIF|tif|jp2)'

    _bandmap = {}

    @classmethod
    def classname(cls):
        """ Lowercase string of class name """
        return cls.__name__.lower()

    def __init__(self, filenames, bandnames=None, basename=None, outpath='./', **kwargs):
        """ Create a scene instance with list of products and filenames """
        # identifier for this scene
        self.basename = self.classname() if basename is None else basename
        # directory to store output products
        self.outpath = outpath
        # a collection of product class instances
        self.__products__ = {n: p(self) for n, p in self._available_products.items()}
        if bandnames is None:
            bandnames = [self.parse_filename(f)[1] for f in filenames]
        self.filenames = dict(zip(bandnames, filenames))
        # the Scene does not open anything - use specific sensor Scene, or
        #  call Scene[product].open() to seed a product with filenames given here

    @classmethod
    def create_from_directory(cls, path):
        """ Create a Scene object from files found in a directory """
        if not os.path.isdir(path):
            raise SatProcessError("directory %s does not exist" % path)
        # match the pattern
        filenames = [os.path.join(path, d) for d in os.listdir(path) if re.match(cls._pattern, d)]
        return cls(filenames)

    def __getattr__(self, attr):
        """ Get processed products as attributes (e.g., scene.ndvi()) """
        if attr not in self.__products__:
            raise SatProcessError("%s product not available in %s" % (attr, self.classname()))
        else:
            return self.__products__[attr].process

    def __getitem__(self, key):
        """ Return GeoImage for this product """
        # TODO - iteratable and other dict-like functions
        if key not in self.__products__:
            raise SatProcessError("%s product not available in %s" % (key, self.classname()))
        return self.__products__[key]

    def available_products(self):
        """ Get list of available products and descriptions """
        # TODO - take into account bands, and what bands available in input products, etc
        return {k: self.__products__[k].description for k in self.__products__.keys()}

    def add_bands(self, product, bands):
        """ Add bands given in self.filenames to product """
        fnames = {f: self.filenames[f] for f in self.filenames if f in bands}
        #import nose.tools; nose.tools.set_trace()
        if len(fnames) > 0:
            self[product].open(filenames=fnames.values(), bandnames=fnames.keys())

    @classmethod
    def parse_filename(cls, filename):
        """ Split out basename and bandname (remapped if in _bandmap) """
        #from nose.tools import set_trace; set_trace()
        m = re.match(cls._pattern, os.path.basename(filename))
        basename = m.group(1)
        bandname = cls._bandmap.get(m.group(2), m.group(2))
        return basename, bandname
