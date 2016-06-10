import product
from errors import SatProcessError


class Scene(object):
    """ A scene is a collection of products (which could be multiple bands) yet
        covers the same (approximate) spatial region and timestamp """

    # available products - override in children
    _available_products = [
        product.DigitalCounts,
        product.TOA,
        product.NDVI,
        product.EVI,
        product.Color,
    ]

    default_product = 'dc'

    @classmethod
    def classname(cls):
        """ Lowercase string of class name """
        return cls.__name__.lower()

    def __init__(self, filenames, basename=None, outpath='./', **kwargs):
        """ Create a scene instance with list of products and filenames """
        # identifier for this scene
        self.basename = self.classname() if basename is None else basename
        # directory to store output products
        self.outpath = outpath
        # a collection of product class instances
        # TODO - look at turning into frozen dictionary after __init__
        self.__products = {p.name: p(self) for p in self._available_products}
        self.__products[self.default_product].open(filenames, **kwargs)

    def __getattr__(self, attr):
        """ Get processed products as attributes (e.g., scene.ndvi()) """
        if attr not in self.__products:
            raise SatProcessError("%s product not available in %s" % (attr, self.classname()))
        else:
            return self.__products[attr].process

    def __getitem__(self, key):
        """ Return GeoImage for this product """
        # TODO - iteratable and other dict-like functions
        if key not in self.__products:
            raise SatProcessError("%s product not available in %s" % (key, self.classname()))
        return self.__products[key]

    def available_products(self):
        """ Get list of available products and descriptions """
        # TODO - take into account bands, and what bands available in input products, etc
        return {k: self.__products[k].description for k in self.__products.keys()}
