#!/usr/bin/env python

import os
import gippy

from process import Process


class Scene(object):
    """ A scene may consist of multiple bands but is for an identical
        spatial footprint and timestamp """

    _products = {
        'pan': {
            'description': 'Pansharpen band using pan band',
            'dependencies': ['pan'],
            'f': Process.pan
        },
        'ndvi': {
            'description': 'Normalized Difference Vegetation Index',
            # these aren't actually products yet
            'dependencies': ['red-toa', 'nir-toa'],
            'f': Process.ndvi
        }
    }

    def __init__(self, filename):
        """ Open a scene as a GeoImage """
        self.path = os.path.dirname(filename)
        self.basename = os.path.basename(os.path.splitext(filename)[0])
        self.open(filename)

    def open(self, products):
        """ Open series of products """
        filenames = [os.path.join(self.path, self.basename) + '_' + p for p in products]
        geoimg = gippy.GeoImage(filenames)
        for i, p in enumerate(products):
            geoimg[i].SetBandName(p)
        return geoimg

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
            fout = os.path.join(self.path, self.basename + '_' + p)
            self.products.func(geoimg, fout, **kwargs)

    @classmethod
    def add_product_parser(cls, parser):
        """ Add arguments to command line parser """
        group = parser.add_argument_group('Products')
        for p, vals in cls._products:
            group.add_argument('--%s' % p, help=vals['description'])
        return parser
