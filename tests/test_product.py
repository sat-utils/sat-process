import unittest
from stestdata import TestData
from sprocess.scene import Scene


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        files = self.t.examples[self.t.examples.keys()[0]]
        self.filenames = []
        self.bandnames = []
        for f in files.values():
            if f['band_type'] != 'pan':
                self.filenames.append(f['path'])
                self.bandnames.append(f['band_type'])

    def test_toa(self):
        """ Get TOA reflectance """
        scene = Scene(self.filenames, bandnames=self.bandnames)
        geoimg = scene.toa()
        self.assertEqual(geoimg.nbands(), len(self.bandnames))
        # should contain same bands
        self.assertEqual(self.bandnames, list(geoimg.bandnames()))

    def test_indices(self):
        """ Index products (e.g., NDVI, EVI) """
        scene = Scene(self.filenames, bandnames=self.bandnames)
        for p in ['ndvi', 'evi']:
            geoimg = scene[p].process()
            self.assertTrue(p in geoimg.bandnames())

    def test_true_color(self):
        """ Make 3 band color byte-scaled image """
        scene = Scene(self.filenames, bandnames=self.bandnames)
        geoimg = scene.color()
        self.assertEquals(geoimg.nbands(), 3)
        self.assertEqual(['red', 'green', 'blue'], list(geoimg.bandnames()))
        with self.assertRaises(Exception):
            geoimg = scene.color(['aqua', 'teal', 'turqouise'])
