#!/usr/bin/env python

import unittest
from satmultispectral import Scene


class TestScene(unittest.TestCase):

    sceneid = 'LC80090612015251LGN00'

    @classmethod
    def setUpClass(cls):
        """ Get test image if not present """
        cls.input_dir = '/home/mhanson/landsat/downloads/%s' % cls.sceneid

    @classmethod
    def tearDownClass(cls):
        """ Clean up after tests """
        pass

    def test_open_from_directory(self):
        """ Test creating a scene from directory of images """
        scene = Scene.open_from_directory(self.input_dir, pattern='*.TIF')
        self.assertTrue(scene.geoimg.Basename, self.sceneid)
