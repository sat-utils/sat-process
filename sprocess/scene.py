#!/usr/bin/env python

import os
import glob
import product
from nose.tools import set_trace


class Scene(object):
    """ A scene may consist of multiple products (which may be multiple bands)
        but covers an identical spatial footprint and timestamp """

    # example available products - each is a Product child class
    _products = {
        product.DC.name(): product.DC,
        product.TOA.name(): product.TOA,
        product.NDVI.name(): product.NDVI,
        # 'color': product.Color,
    }

    def __init__(self, products, basename=''):
        """ Create a Scene instance with list of Product classes """
        # save in dictionary with key as product name
        self.products = {p.name(): p for p in products}
        self.basename = basename

    def available_products(self):
        """ Get list of available products (based on existing products) """
        # TODO - take into account bands, and what bands available in input products, etc
        return self._products.keys()

    def process(self, product, outfile=None, outpath='./', **kwargs):
        """ Process this product if not already processed """
        if product not in self._products.keys():
            raise IOError("Product %s not available" % product)
        # if not already processed
        if product not in self.products:
            # process dependencies
            depend = self._products[product].dependencies
            for d in depend:
                # what about passing in options when dependencies processed in this way?
                self.process(d)
            input_products = [self.products[d] for d in depend]
            # create new product from dependencies as input
            self.products[product] = self._products[product](input_products)

        # saving and processing product, get geomage ?
        if outfile is None:
            outfile = os.path.join(outpath, self.basename + '_' + product)

        return self.products[product].process(outfile=outfile, **kwargs)

    @classmethod
    def seed_from_filenames(cls, filenames, **kwargs):
        """ Parse a list of filenames and seed a scene """
        products = []
        for p in cls._products:
            prod = cls._products[p].create_from_filenames(filenames)
            if prod is not None:
                products.append(prod)
        return cls(products, **kwargs)

    # @classmethod
    # def seed_from_filenames_dict(cls, filenames, **kwargs):
    #    """ Factory to create Scene from dictionary of filenames {product: {band: filename}} """
    #    products = [cls._products[p](filenames[p]) for p in filenames]
    #    return cls(products, **kwargs)

    @classmethod
    def seed_from_directory(cls, directory):
        """ Factory to create scene from dir of files """
        filenames = glob.glob(os.path.join(directory, '*'))
        if len(filenames) == 0:
            raise IOError("No scene data found in directory %s" % directory)
        return cls.seed_from_filenames(filenames)

    @classmethod
    def add_product_parser(cls, parser):
        """ Add arguments to command line parser """
        # TODO - right now only T/F switches, no args handled
        group = parser.add_argument_group('Products')
        for p, prod in cls._products.items():
            # if vals['args'] is None:
            group.add_argument('--%s' % p, help=prod['description'], default=False, action='store_true')
            # else:
            #    group.add_argument('--%s' % p, help=vals['description'], nargs='%s' % len(vals['args']))
        return parser
