import unittest
from stestdata import TestData
from sprocess.sentinel2 import Sentinel2


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('sentinel2')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        scene = Sentinel2(self.filenames[0])
        self.assertEqual(scene.product_name('ndvi'), 'ndvi_B01')

    def test_ndvi(self):
        scene = Sentinel2(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.band_numbers, 8)

        scene.ndvi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('ndvi' in scene.bands)

    def test_evi(self):
        scene = Sentinel2(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.band_numbers, 8)

        scene.evi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('evi' in scene.bands)

    def test_process_chaining(self):
        scene = Sentinel2(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.band_numbers, 8)

        scene.ndvi().evi()
        self.assertEquals(scene.band_numbers, 10)
        self.assertTrue('evi' in scene.bands)
        self.assertTrue('ndvi' in scene.bands)
