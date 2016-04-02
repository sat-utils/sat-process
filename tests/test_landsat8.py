#!/usr/bin/env python

from test_scene import _BaseTestScene
import gippy
from satmultispectral.landsat8 import Landsat8Scene


class _TestLandsat8(_BaseTestScene):

    scene = Landsat8Scene
    sceneid = 'LC80090612015251LGN00'

    @classmethod
    def setUpClass(cls):
        """ Get test image if not present """
        gippy.Options.SetVerbose(3)
        cls.input_dir = '/home/mhanson/landsat/downloads/%s' % cls.sceneid
