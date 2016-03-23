#!/usr/bin/env python

from scene import Scene
import gippy.algorithms as algs


class Landsat8Scene(Scene):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _bands = {
        'B1': 'coastal',
        'B2': 'blue',
        'B3': 'green',
        'B4': 'red',
        'B5': 'nir',
        'B6': 'swir1',
        'B7': 'swir22',
        'B8': 'pan',
        'B9': 'cirrus',
        # don't bother with longwave right now
        # 'B10': 'lwir1',
        # 'B11': 'lwir2',
        'BQA': 'quality'
    }

    _products = {
        'coastal': {
            'description': 'Coastal band (~0.43um) TOA',
            'dependencies': [],
            'args': None,
            'f': None,
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
            'dependencies': ['red', 'nir'],
            'f': (lambda geoimg, fout: algs.Indices(geoimg, {'ndvi': fout})),
        }
        #'pansharpen': {
        #    'description': 'Pansharpen band using pan band',
        #    'dependencies': ['pan'],
        #    'f': algs.pan,
        #    'args': None
        #},
    }

    _pattern = '*.TIF'

    @classmethod
    def open(cls, filenames):
        """ Open a Landsat8 scene """
        geoimg = super(Landsat8Scene, cls).open(filenames)
        geoimg.SetNoData(0)
        # read MTL and set data on self.geoimg
        # get gains/offsets for radiance, reflectance, etc.
        # get clouds, dynamic range
        # get geometry
        return geoimg
