import unittest
from stestdata import TestData
from satprocess.scene import Scene
from nose.tools import set_trace


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        files = self.t.examples[self.t.examples.keys()[0]]
        self.filenames = []
        self.bandnames = []
        for f in files.values():
            if f['band_type'] not in ['pan', 'quality']:
                self.filenames.append(f['path'])
                self.bandnames.append(f['band_type'])

    def get_scene(self, **kwargs):
        """ Get a scene for testing """
        scene = Scene(self.filenames, **kwargs)
        scene['dc'].open()
        return scene

    def test_toa(self):
        """ Get TOA reflectance """
        scene = self.get_scene(bandnames=self.bandnames)
        geoimg = scene.toa()
        self.assertEqual(geoimg.nbands(), len(self.bandnames))
        # should contain same bands
        for b in self.bandnames:
            self.assertTrue(b in geoimg.bandnames())

    def test_indices(self):
        """ Index products (e.g., NDVI, EVI) """
        scene = self.get_scene(bandnames=self.bandnames)
        for p in ['ndvi', 'evi']:
            geoimg = scene[p].process()
            self.assertTrue(p in geoimg.bandnames())

    def test_true_color(self):
        """ Make 3 band color byte-scaled image """
        scene = self.get_scene(bandnames=self.bandnames)
        geoimg = scene.color()
        self.assertEquals(geoimg.nbands(), 3)
        self.assertEqual(['red', 'green', 'blue'], list(geoimg.bandnames()))
        with self.assertRaises(Exception):
            geoimg = scene.color(['aqua', 'teal', 'turqouise'])
