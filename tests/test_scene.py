#!/usr/bin/env python

import os
import unittest
from sprocess import Scene
import gippy


class _BaseTestScene(unittest.TestCase):

    scene = Scene

    sceneid = 'test'

    testdir = os.path.join(os.path.dirname(__file__), 'images')

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.testdir):
            os.mkdir(cls.testdir)

    @classmethod
    def tearDownClass(cls):
        """ Clean up after tests """
        print 'remove ndvi-test.tif'
        # os.remove('ndvi-test.tif')

    def test_create_from_directory(self):
        """ Test creating a scene from directory of images """
        scene = self.scene.seed_from_directory(self.testdir)
        geoimg = scene.process('toa')
        self.assertTrue(geoimg.Basename(), self.sceneid)

    # generalize this into loop through test all products
    def test_ndvi(self):
        """ Test calculating NDVI product """
        scene = self.scene.seed_from_directory(self.testdir)
        scene.process('ndvi', outfile=os.path.join(self.testdir, '%s_ndvi.tif' % self.sceneid))
        # check with numpy against original band
        #geoimg1 = scene.products['']


class TestScene(_BaseTestScene):
    """ Perform testing with generic images """

    @classmethod
    def setUpClass(cls):
        """ Create some test images """
        super(TestScene, cls).setUpClass()
        fout = os.path.join(cls.testdir, '%s_dc.tif' % cls.sceneid)
        if not os.path.exists(fout):
            geoimg = gippy.GeoImage(fout, 100, 100, 4, gippy.DataType('Float64'))
            # geoimg.SetBandNames(['blue', 'green', 'red', 'nir'])
            geoimg.SetBandName('blue', 1)
            geoimg.SetBandName('green', 2)
            geoimg.SetBandName('red', 3)
            geoimg.SetBandName('nir', 4)
        else:
            geoimg = gippy.GeoImage(fout)
        geoimg['nir'] = geoimg['nir'] + 2
        geoimg['red'] = geoimg['red'] + 1
        # save with some values for nir and red
        geoimg.Process()
        geoimg = None
