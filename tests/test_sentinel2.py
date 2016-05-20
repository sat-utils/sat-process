import os
import shutil
import unittest
import rasterio
import numpy as np
from tempfile import mkdtemp
from stestdata import TestData
from sprocess.sentinel2 import Sentinel2
from sprocess.errors import SatProcessError


class TestProduct(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def setUp(self):
        self.t = TestData('sentinel2')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        scene = Sentinel2(self.filenames)
        self.assertEqual(len(scene.bandnames()), len(scene.filenames()))
        self.assertEqual(scene.bandnames()[0], 'coastal')

    def test_color_correction(self):
        scene = Sentinel2(self.filenames)
        scene.set_bandnames(self.bandnames)

        bands = ['red', 'green', 'blue']
        rgb = scene.select(bands)

        scene = scene.color_correction(bands=bands)
        for key in bands:
            self.assertFalse(np.array_equal(rgb[key], scene[key]))

    def test_true_color(self):
        scene = Sentinel2(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.nbands(), 8)

        f = os.path.join(self.tmp, 'tcolor.tif')

        scene.color_correction(2).true_color(f)

        # open file and make sure it has three bands
        with rasterio.drivers():
            with rasterio.open(f, 'r') as src:
                self.assertEquals(len(src.indexes), 3)
                shutil.copyfile(f, 'set.tif')
                # self.assertTrue(np.array_equal(src.read(1), scene['red'].read()))

    def test_ndvi(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        ndvi = scene.ndvi()
        self.assertEquals(ndvi.band_numbers, 9)
        self.assertTrue('ndvi' in ndvi.bands)

    def test_ndvi_incorrect_bands(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        scene2 = scene.select(['red', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'Band nir is required')

        scene2 = scene.select(['nir', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'Band red is required')
