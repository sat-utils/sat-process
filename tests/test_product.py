import os
import shutil
import unittest
import rasterio
import numpy as np
from tempfile import mkdtemp
from stestdata import TestData
from sprocess.scene import Scene
from sprocess.errors import SatProcessError
from sprocess.product import NDVI, TrueColor, ColorCorrection, SnowCoverage


class SceneProductForTest(Scene, NDVI, TrueColor, ColorCorrection, SnowCoverage):
    """ Since Product is a mixin class we have to mix it with scene in order to be able
    to properly test it """
    pass


class TestProduct(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_snow_cloud_coverage(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)

        self.assertAlmostEqual(scene.snow_cloud_coverage(), 6.025, 2)

        # try with the quality band missing
        scene.delete(['quality'])

        with self.assertRaises(SatProcessError):
            scene.snow_cloud_coverage()

    def test_color_correction(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)

        bands = ['red', 'green', 'blue']
        rgb = scene.select(bands)

        scene = scene.color_correction(bands=bands)
        for key in bands:
            self.assertFalse(np.array_equal(rgb[key], scene[key]))

    def test_true_color(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.nbands(), 10)

        f = os.path.join(self.tmp, 'tcolor.tif')
        scene.true_color(f)

        # open file and make sure it has three bands
        with rasterio.drivers():
            with rasterio.open(f, 'r') as src:
                self.assertEquals(len(src.indexes), 3)
                self.assertTrue(np.array_equal(src.read(1), scene['red'].read()))

    def test_ndvi(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.nbands(), 10)

        scene.ndvi()
        self.assertEquals(scene.nbands(), 11)
        self.assertTrue('ndvi' in scene.bands)
        self.assertEquals(scene['ndvi'].read().size, scene['red'].read().size)
