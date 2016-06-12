import unittest
import os
from gippy import GeoImage
from stestdata import TestData
from satprocess.scene import Scene
from nose.tools import set_trace

class TestScene(unittest.TestCase):
    """ Test default scene with DC, TOA, and NDVI products """

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
        scene = Scene(self.filenames, **kwargs)
        # generic scene, so need to open those files as one of the prroducts
        scene['dc'].open()
        return scene

    def test_scene(self):
        """ Create Scene object with only filenames """
        scene = self.get_scene(bandnames=self.bandnames)
        geoimg = scene.dc()
        self.assertTrue(isinstance(geoimg, GeoImage))
        for b in self.bandnames:
            self.assertTrue(b in geoimg.bandnames())

    def test_scene_bands(self):
        """ Test creation of Scene object with filenames and bands"""
        scene = self.get_scene(bandnames=self.bandnames)
        geoimg = scene.dc()
        self.assertTrue(isinstance(geoimg.bandnames(), tuple))
        self.assertEqual(geoimg.nbands(), len(self.bandnames))

    def test_scene_invalid(self):
        """ Test invalid inputs raise exceptions """
        with self.assertRaises(Exception):
            Scene('path/to/file')

        with self.assertRaises(Exception):
            Scene({'path/to/file': 'red'})

    def test_scene_basename(self):
        """ Basename of scene """
        scene = self.get_scene()
        geoimg = scene.dc()
        bname = os.path.basename(os.path.splitext(self.filenames[0])[0])
        self.assertEqual(geoimg.basename(), bname)
