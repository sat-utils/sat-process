import unittest
from stestdata import TestData
from satprocess.landsat8 import Landsat8Scene
from satprocess.errors import SatProcessError


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        """ Read in and process scene """
        scene = Landsat8Scene(self.filenames)
        geoimg = scene.toa()
        self.assertEqual(len(geoimg.bandnames()), 8)
        for b in self.bandnames:
            if b not in ['quality', 'pan']:
                self.assertTrue(b in geoimg.bandnames())

    def test_ndvi(self):
        """ NDVI (red, nir) """
        scene = Landsat8Scene(self.filenames)
        geoimg = scene.ndvi()
        self.assertEquals(geoimg.nbands(), 1)
        self.assertTrue('ndvi' in geoimg.bandnames())

    def _test_ndvi_incorrect_bands(self):
        """ NDVI with wrong bands """
        scene = Landsat8Scene(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'nir band is not provided')

        scene2 = scene.select(['nir', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'red band is not provided')

    def test_evi(self):
        """ EVI (nir, red, blue) """
        scene = Landsat8Scene(self.filenames)
        geoimg = scene.evi()
        self.assertEquals(geoimg.nbands(), 1)
        self.assertTrue('evi' in geoimg.bandnames())
