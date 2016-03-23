#!/usr/bin/env python

import os
import glob
import gippy
import gippy.algorithms as algs

from nose.tools import set_trace

""" Create a Scene with dictionary of filenames indicating filename for each
    band """


class Scene(object):
    """ A scene may consist of multiple bands but is for an identical
        spatial footprint and timestamp """

    # example band filename designator vs standard band names, override in child class
    _bands = {
        'B1': 'Red',
        'B2': 'Green',
        'B3': 'Blue',
        'B4': 'NIR',
    }

    # example products
    _products = {
        'coastal': {
            'description': 'Coastal band (~0.43um) TOA',
            'dependencies': [],
            'args': None,
            'f': None,
        },
        'pan': {
            'description': 'Panchromatic band TOA',
        },
        'blue': {
            'description': 'Blue band TOA',
        },
        'green': {
            'description': 'Green band TOA',
        },
        'red': {
            'description': 'Red band TOA',
        },
        'nir': {
            'description': 'Near IR band TOA',
        },
        'cirrus': {
            'description': 'Cirrus cloud detection band (~1.38um) TOA',
        },
        'swir1': {
            'description': 'Shortwave IR band (~1.65um) TOA',
        },
        'swir2': {
            'description': 'Shortwave IR band (~2.2um) TOA',
        },

        # derived products
        'ndvi': {
            'description': 'Normalized Difference Vegetation Index from TOA reflectance',
            'dependencies': ['RED', 'NIR'],
            'f': (lambda geoimg, fout, **kwargs: algs.Indices(geoimg, {'NDVI': fout})),
        }
    }

    def __init__(self, filenames):
        """ Create a Scene instance with dict of {product: filename, ...} """
        try:
            self.open(filenames)
        # TODO better exception handling
        except Exception, e:
            print e
            raise Exception('unable to create image')
        # this is current list of available products
        self.products = filenames

    def open_products(self, products):
        """ Get GeoImage of these products [prod1, prod2] """
        # all requested products available
        assert all([p in self.products for p in products])
        return self.open({p: self.products[p] for p in products})

    def open_all_products(self):
        """ Get GeoImage of all products """
        return self.open(self.products)

    @classmethod
    def open(cls, filenames):
        """ Open series of products """
        bands = sorted(filenames.keys())
        fnames = [filenames[f] for f in sorted(filenames.keys())]
        geoimg = gippy.GeoImage(fnames)
        for i, b in enumerate(bands):
            geoimg.SetBandName(b, i+1)
        return geoimg

    def process(self, products):
        """ Generate these products for this scene {'product': {options}} """
        for p in products:
            # if not already available
            if p not in self.products:
                depend = self._products[p].get('dependencies')
                print p, self._products
                if not depend:
                    raise IOError("Product %s not available" % p)
                if depend:
                    # process dependencies without options
                    self.process({d: {} for d in depend})
                    # open GeoImage of dependencies
                    geoimg = self.open_products(depend)
                    # process into product
                    kwargs = products[p]
                    if 'fout' in kwargs:
                        fout = kwargs['fout']
                        del kwargs['fout']
                    else:
                        # create filename based on input and product name
                        fout = os.path.join(self.path, geoimg.Basename() + '_' + p)
                    # call product function
                    self._products[p]['f'](geoimg, fout, **kwargs)
                    # save to current list of available products
                    self.products[p] = fout

    @classmethod
    def parse_directory(cls, directory, pattern='*.TIF'):
        """ Parse a directory for files with a _product suffix """
        assert os.path.isdir(directory)
        found = glob.glob(os.path.join(directory, pattern))
        filenames = {}
        for f in found:
            bname = os.path.basename(os.path.splitext(f)[0])
            ind = bname.rfind('_')
            if ind != -1:
                product = bname[ind+1:]
                if product in cls._bands.keys():
                    # use standard band name
                    filenames[cls._bands[product]] = f
                if product in cls._products.keys():
                    # or if already existing product
                    filenames[product] = f
        return filenames

    @classmethod
    def create_from_directory(cls, directory, pattern='*.TIF'):
        """ Factory function to create scene from dir of products
            where filename is in the form sceneid_product """
        filenames = cls.parse_directory(directory, pattern=pattern)
        if len(filenames) > 0:
            return cls(filenames)
        else:
            raise IOError("No scene data found in directory %s" % directory)

    @classmethod
    def add_product_parser(cls, parser):
        """ Add arguments to command line parser """
        # TODO - right now only T/F switches, no args handled
        group = parser.add_argument_group('Products')
        for p, prod in cls._products.items():
            #if vals['args'] is None:
            group.add_argument('--%s' % p, help=prod['description'], default=False, action='store_true')
            #else:
            #    group.add_argument('--%s' % p, help=vals['description'], nargs='%s' % len(vals['args']))
        return parser
