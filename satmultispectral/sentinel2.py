#!/usr/bin/env python

from scene import Scene
import gippy.algorithms as algs


class Sentinel2Scene(Scene):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _bands = {
        'B01': 'coastal',
        'B02': 'blue',
        'B03': 'green',
        'B04': 'red',
        'B08': 'nir',
        'B10': 'cirrus',
        'B11': 'swir1',
        'B12': 'swir2'
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
            'dependencies': ['RED', 'NIR'],
            'f': (lambda geoimg, fout, **kwargs: algs.Indices(geoimg, {'NDVI': fout})),
        }
    }

    _pattern = '*.jp2'

    def open(self, filenames):
        """ Open a Landsat8 scene """
        super(Sentinel2Scene, self).open(filenames)
        self.geoimg.SetNoData(0)
        # read MTL and set data on self.geoimg
        # get gains/offsets for radiance, reflectance, etc.
        # get clouds, dynamic range
        # get geometry
