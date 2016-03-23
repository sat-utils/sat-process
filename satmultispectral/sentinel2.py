#!/usr/bin/env python

from scene import Scene
import gippy.algorithms as algs


class SentinelScene(object):
    """ A tile of Sentinel data for same timestamp and spatial region
        and possibly containing multiple bands """

    _bands = {
        1: 'Coastal',
        2: 'Blue',
        3: 'Green',
        4: 'Red',
        8: 'NIR',
        10: 'Cirrus',
        11: 'SWIR1',
        12: 'SWIR2'
    }
