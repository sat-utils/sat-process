from .base import BaseTest
from sprocess.sentinel2 import Sentinel2


class TestProduct(BaseTest):

    def setUp(self):
        super(TestProduct, self).setUp(path='samples/sentinel2', extension='jp2', scenes=Sentinel2.bands_map)

    def test_product_name(self):
        scene = Sentinel2({self.files[0]: ['red']})
        scene.open()
        self.assertEqual(scene.product_name('ndvi'), 'ndvi_B01.jp2')

    def test_ndvi(self):
        scene = Sentinel2(self.file_dict)
        scene.open()
        self.assertEquals(scene.band_numbers, 8)

        scene.open().ndvi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('ndvi' in scene.bands)

    def test_evi(self):
        scene = Sentinel2(self.file_dict)
        scene.open()
        self.assertEquals(scene.band_numbers, 8)

        scene.open().evi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('evi' in scene.bands)

    def test_process_chaining(self):
        scene = Sentinel2(self.file_dict)
        scene.open()
        self.assertEquals(scene.band_numbers, 8)

        scene.open().ndvi().evi()
        self.assertEquals(scene.band_numbers, 10)
        self.assertTrue('evi' in scene.bands)
        self.assertTrue('ndvi' in scene.bands)
