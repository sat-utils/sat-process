import unittest
import os
from gippy import GeoImage
from stestdata import TestData
from sprocess.scene import Scene


class TestScene(unittest.TestCase):
    """ Test default scene with DC, TOA, and NDVI products """

    def setUp(self):
        self.t = TestData('landsat8')
        files = self.t.examples[self.t.examples.keys()[0]]
        self.filenames = []
        self.bandnames = []
        for f in files.values():
            if f['band_type'] != 'pan':
                self.filenames.append(f['path'])
                self.bandnames.append(f['band_type'])

    def test_scene(self):
        """ Test creation of Scene object with only filenames """
        scene = Scene(self.filenames)
        geoimg = scene.dc()
        self.assertTrue(isinstance(geoimg, GeoImage))
        self.assertEqual(geoimg.nbands(), len(self.filenames))

    def test_scene_bands(self):
        """ Test creation of Scene object with filenames and bands"""
        scene = Scene(self.filenames, bandnames=self.bandnames)
        geoimg = scene.dc()
        self.assertTrue(isinstance(geoimg.bandnames(), tuple))
        self.assertEqual(geoimg.nbands(), len(self.bandnames))
        self.assertEqual(list(geoimg.bandnames()), self.bandnames)

    def test_scene_invalid(self):
        """ Test invalid inputs raise exceptions """
        with self.assertRaises(Exception):
            Scene('path/to/file')

        with self.assertRaises(Exception):
            Scene({'path/to/file': 'red'})

    def test_scene_basename(self):
        scene = Scene([self.filenames[0]])
        geoimg = scene.dc()
        bname = os.path.basename(os.path.splitext(self.filenames[0])[0])
        self.assertEqual(geoimg.basename(), bname)
