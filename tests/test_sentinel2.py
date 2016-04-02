#!/usr/bin/env python

from test_scene import _BaseTestScene
import unittest
from sprocess.sentinel2 import Sentinel2Scene


class _TestSentinel2(_BaseTestScene):

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

    def test_save_toa(self):
        """ Save original files to GeoTiff """
        scene = self.scene.seed_from_directory(self.input_dir)
        scene.process('toa', outpath=self.testdir)


