import unittest
from stestdata import TestData
from sprocess.landsat8 import Landsat8
from sprocess.errors import SatProcessError


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        scene = Landsat8(self.filenames)
        self.assertEqual(len(scene.bandnames()), len(scene.filenames()))
        self.assertEqual(scene.bandnames()[0], 'coastal')

    def test_ndvi(self):
        scene = Landsat8(self.filenames)
        self.assertEquals(scene.band_numbers, 10)

        scene.ndvi()
        self.assertEquals(scene.band_numbers, 11)
        self.assertTrue('ndvi' in scene.bands)

    def test_ndvi_incorrect_bands(self):
        scene = Landsat8(self.filenames)
        self.assertEquals(scene.band_numbers, 10)

        scene2 = scene.select(['red', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'nir band is not provided')

        scene2 = scene.select(['nir', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'red band is not provided')
