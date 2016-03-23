#!/usr/bin/env python

from test_scene import _TestScene
import unittest
import gippy
from satmultispectral.landsat8 import Landsat8Scene


class TestLandsat8(_TestScene):

    scene = Landsat8Scene
    sceneid = 'LC80090612015251LGN00'

    @classmethod
    def setUpClass(cls):
        """ Get test image if not present """
        gippy.Options.SetVerbose(3)
        cls.input_dir = '/home/mhanson/landsat/downloads/%s' % cls.sceneid
