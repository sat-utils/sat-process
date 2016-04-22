import unittest
from stestdata import TestData
from sprocess.landsat8 import Landsat8


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        scene = Landsat8(self.filenames)
        self.assertEqual(len(scene.bandnames()), len(scene.filenames()))
        self.assertEqual(scene.bandnames()[0], 'coastal')
