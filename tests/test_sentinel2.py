#!/usr/bin/env python

from test_scene import _TestScene
import unittest
from satmultispectral.sentinel2 import Sentinel2Scene


class TestSentinel2(_TestScene):

    scene = Sentinel2Scene
    sceneid = 'test'

    @classmethod
    def setUpClass(cls):
        """ Get test image if not present """
        cls.input_dir = '/home/mhanson/data/sentinel/%s' % cls.sceneid

    @classmethod
    def tearDownClass(cls):
        """ Clean up after tests """
        pass
