import unittest
from gippy import GeoImage
from sprocess import errors
from stestdata import TestData
from sprocess.scene import Scene


class TestScene(unittest.TestCase):

    def setUp(self):
        self.t = TestData('landsat8')

    def test_scene_filenames_only(self):
        """ Test creation of Scene object with only filenames """
        images = Scene(self.t.files[self.t.names[0]])
        imgs = images.open()
        self.assertTrue(isinstance(imgs, GeoImage))
        self.assertEqual(imgs.nbands(), len(self.t.files[self.t.names[0]]))

    def test_scene_filenames_and_bands(self):
        """ Test creation of Scene object with filenames and bands"""

        images = Scene(self.t.files_bands[self.t.names[0]])
        images.open()
        self.assertTrue(images.is_open)
        self.assertEqual(images.geoimg.nbands(), len(self.t.files_bands[self.t.names[0]]))

    def test_scene_wrong_input(self):

        with self.assertRaises(Exception):
            Scene('path/to/file')

        with self.assertRaises(Exception):
            Scene({'path/to/file': 'red'})

    def test_scene_bands(self):
        scene = Scene(self.t.files_bands[self.t.names[0]])

        # Get band names before opening the files
        with self.assertRaises(errors.SceneIsNotOpen):
            scene.bands

        # Get bands names after opening the files
        scene.open()
        bands = scene.bands
        self.assertTrue(isinstance(bands, tuple))
        self.assertEqual(len(bands), 10)

    def test_scene_basename(self):
        scene = Scene([self.t.files[self.t.names[0]][0]])
        scene.open()
        self.assertEqual(scene.basename(), 'test_B1.tif')
