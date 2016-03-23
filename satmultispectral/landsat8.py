#!/usr/bin/env python

from scene import Scene
import gippy.algorithms as algs


class Landsat8Scene(object):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _bands = {
        1: 'Coastal',
        2: 'Blue',
        3: 'Green',
        4: 'Red',
        5: 'NIR',
        6: 'SWIR1',
        7: 'SWIR2',
        8: 'Pan',
        9: 'Cirrus',
        10: 'LWIR1',
        11: 'LWIR2'
    }

    def SetMeta(self):
        """ Set metadata on scene """
        self.geoimg.SetNoData(0)
        # read MTL and set data on self.geoimg
        # get gains/offsets for radiance, reflectance, etc.
        # get clouds, dynamic range
        # get geometry
