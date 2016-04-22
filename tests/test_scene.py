import unittest
from gippy import GeoImage
from stestdata import TestData
from sprocess.scene import Scene


class TestScene(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_scene_filenames_only(self):
        """ Test creation of Scene object with only filenames """
        images = Scene(self.filenames)
        self.assertTrue(isinstance(images, GeoImage))
        self.assertEqual(images.nbands(), len(self.t.files[self.t.names[0]]))

    def test_scene_filenames_and_bands(self):
        """ Test creation of Scene object with filenames and bands"""

        images = Scene(self.filenames)
        self.assertEqual(images.nbands(), len(self.filenames))

    def test_scene_wrong_input(self):

        with self.assertRaises(Exception):
            Scene('path/to/file')

        with self.assertRaises(Exception):
            Scene({'path/to/file': 'red'})

    def test_scene_bands(self):
        scene = Scene(self.filenames)
        # Get bands names after opening the files
        bands = scene.bands
        self.assertTrue(isinstance(bands, tuple))
        self.assertEqual(len(bands), 10)

    def test_scene_basename(self):
        scene = Scene([self.t.files[self.t.names[0]][0]])
        self.assertEqual(scene.basename(), 'test_B1')
