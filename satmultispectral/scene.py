#!/usr/bin/env python

import os
import glob
import gippy
import gippy.algorithms as algs

from process import Process

""" Create a Scene with dictionary of filenames indicating filename for each
    band """


class Scene(object):
    """ A scene may consist of multiple bands but is for an identical
        spatial footprint and timestamp """

    _products = {
        'rad': {
            'description': 'Apparent radiance',
            'dependencies': [],
            'args': None,
            'f': None,
        },
        'ref': {
            'description': 'Top of the Atmosphere Reflectance',
            'dependencies': [],
            'args': None,
            'f': None,
        },
        'pan': {
            'description': 'Pansharpen band using pan band',
            'dependencies': ['pan'],
            'f': algs.pan,
            'args': None
        },
        'ndvi': {
            'description': 'Normalized Difference Vegetation Index from TOA reflectance',
            # these aren't actually products yet
            'dependencies': ['red-toa', 'nir-toa'],
            'f': algs.ndvi,
            'args': ['color'],
        }
    }

    @classmethod
    def open_from_directory(cls, directory, pattern='*.TIF'):
        """ Factory function to create scene from dir of products """
        assert os.path.isdir(directory)
        found = glob.glob(os.path.join(directory, pattern))
        filenames = {}
        for f in found:
            bname = os.path.basename(os.path.splitext(f)[0])
            ind = bname.rfind('_')
            if ind != -1:
                product = bname[ind+1:]
                if product in cls._products.keys():
                    print 'here'
                    filenames[product] = f
        if len(filenames) > 0:
            return cls(filenames)
        else:
            return None

    def __init__(self, filenames):
        """ Create a Scene instance with dict of {product: filename, ...} """
        self.open(filenames)

    def open(self, filenames):
        """ Open series of products """
        bands = sorted(filenames.keys())
        fnames = [filenames[f] for f in sorted(filenames.keys())]
        self.geoimg = gippy.GeoImage(fnames)
        for i, b in enumerate(bands):
            self.geoimg.SetBandName(b, i+1)
        return self.geoimg

    def process(self, products):
        """ Generate these products for this scene """
        for p in products:
            depend = self._products[p]['dependencies']
            # process dependencies
            self.process(depend)
            # open GeoImage of dependencies
            geoimg = self.open(depend)

            # process into product
            kwargs = products[p]
            fout = os.path.join(self.path, self.geoimg.Basename() + '_' + p)
            self._products['f'](geoimg, fout, **kwargs)

    def set_metadata(self):
        """ Set custom metadata on geoimg based on sensor """
        pass

    @classmethod
    def add_product_parser(cls, parser):
        """ Add arguments to command line parser """
        group = parser.add_argument_group('Products')
        for p, vals in cls._products.items():
            #if vals['args'] is None:
            group.add_argument('--%s' % p, help=vals['description'], default=False, action='store_true')
            #else:
            #    group.add_argument('--%s' % p, help=vals['description'], nargs='%s' % len(vals['args']))
        return parser
