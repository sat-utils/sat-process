import unittest
from stestdata import TestData
from sprocess.scene import Scene
from sprocess.product import NDVI, EVI, TrueColor


class SceneProductForTest(Scene, NDVI, EVI, TrueColor):
    """ Since Product is a mixin class we have to mix it with scene in order to be able
    to properly test it """
    pass


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        band = self.t.examples[self.t.names[0]]['B1']['path']
        scene = SceneProductForTest([band])
        self.assertEqual(scene.product_name('ndvi'), 'ndvi_test_B1')

    def test_true_color(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.nbands(), 10)

        true_color = scene.true_color()
        self.assertEquals(true_color.nbands(), 3)
        self.assertTrue('red' == true_color.bands[0])

    def test_ndvi(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.nbands(), 10)

        ndvi = scene.ndvi()
        self.assertEquals(ndvi.nbands(), 1)
        self.assertTrue('ndvi' in ndvi.bands)

    def test_evi(self):
        scene = SceneProductForTest(self.filenames)
        scene.set_bandnames(self.bandnames)
        self.assertEquals(scene.band_numbers, 10)

        evi = scene.evi()
        self.assertEquals(evi.band_numbers, 1)
        self.assertTrue('evi' in evi.bands)
