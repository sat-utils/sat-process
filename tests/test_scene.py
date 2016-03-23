#!/usr/bin/env python

import os
import unittest
from satmultispectral import Scene
from nose.tools import set_trace


class _TestScene(unittest.TestCase):

    scene = Scene

    @classmethod
    def tearDownClass(cls):
        """ Clean up after tests """
        print 'remove ndvi-test.tif'
        # os.remove('ndvi-test.tif')

    def create_from_directory(self):
        """ Open test image from directory """
        return self.scene.create_from_directory(self.input_dir, pattern=self.scene._pattern)

    def _test_create_from_directory(self):
        """ Test creating a scene from directory of images """
        scene = self.create_from_directory()
        geoimg = scene.open_all_products()
        self.assertTrue(geoimg.Basename, self.sceneid)

    # generalize this into loop through test all products
    def test_ndvi(self):
        """ Test calculating NDVI product """
        scene = self.create_from_directory()
        scene.process({'ndvi': {'fout': 'tests/%s_test-ndvi.tif' % self.sceneid}})
