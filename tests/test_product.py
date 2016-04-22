import unittest
from stestdata import TestData
from sprocess.scene import Scene
from sprocess.product import NDVI, EVI


class SceneProductForTest(Scene, NDVI, EVI):
    """ Since Product is a mixin class we have to mix it with scene in order to be able
    to properly test it """
    pass


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')

    def test_product_name(self):
        band = self.t.examples[self.t.names[0]]['B1']['path']
        scene = SceneProductForTest([band])
        scene.open()
        self.assertEqual(scene.product_name('ndvi'), 'ndvi_test_B1.tif')

    def test_ndvi(self):
        scene = SceneProductForTest(self.t.files_bands[self.t.names[0]])
        scene.open()
        self.assertEquals(scene.band_numbers, 10)

        scene.open().ndvi()
        self.assertEquals(scene.band_numbers, 11)
        self.assertTrue('ndvi' in scene.bands)

    def test_evi(self):
        scene = SceneProductForTest(self.t.files_bands[self.t.names[0]])
        scene.open()
        self.assertEquals(scene.band_numbers, 10)

        scene.open().evi()
        self.assertEquals(scene.band_numbers, 11)
        self.assertTrue('evi' in scene.bands)

    def test_process_chaining(self):
        scene = SceneProductForTest(self.t.files_bands[self.t.names[0]])
        scene.open()
        self.assertEquals(scene.band_numbers, 10)

        scene.open().ndvi().evi()
        self.assertEquals(scene.band_numbers, 12)
        self.assertTrue('evi' in scene.bands)
        self.assertTrue('ndvi' in scene.bands)
