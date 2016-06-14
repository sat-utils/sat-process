import unittest
from stestdata import TestData
from satprocess.sentinel2 import Sentinel2Scene
from satprocess.errors import SatProcessError


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('sentinel2')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_visbands(self):
        """ Check visible bands present """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.toa()
        self.assertEqual(geoimg.nbands(), 4)
        for b in geoimg.bandnames():
            self.assertTrue(b in ['red', 'green', 'blue', 'nir'])

    def test_swirbands(self):
        """ Check swir bands present """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.swir()
        self.assertEqual(geoimg.nbands(), 2)
        for b in geoimg.bandnames():
            self.assertTrue(b in ['swir1', 'swir2'])

    def test_cbands(self):
        """ Check cloud bands present """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.cbands()
        self.assertEqual(geoimg.nbands(), 2)
        for b in geoimg.bandnames():
            self.assertTrue(b in ['coastal', 'cirrus'])

    def test_ndvi(self):
        """ Generate NDVI product (red, nir) """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.ndvi()
        self.assertEquals(geoimg.nbands(), 1)
        self.assertTrue('ndvi' in geoimg.bandnames())

    def test_incorrect_bands(self):
        """ Generate NDVI without bands available """
        scene = Sentinel2Scene(self.filenames)
        scene["toa"].geoimg = scene["toa"].geoimg.select(['green', 'blue', 'nir'])
        try:
            scene.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'ndvi requires bands: nir red')

    def test_evi(self):
        """ EVI (nir, red, blue) """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.evi()
        self.assertEquals(geoimg.nbands(), 1)
        self.assertTrue('evi' in geoimg.bandnames())

    def test_color(self):
        """ Generate TrueColor product """
        scene = Sentinel2Scene(self.filenames)
        geoimg = scene.color()
        self.assertEqual(geoimg.nbands(), 3)
        for b in geoimg.bandnames():
            self.assertTrue(b in ['red', 'green', 'blue'])
