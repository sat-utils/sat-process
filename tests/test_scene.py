from gippy import GeoImage
from .base import BaseTest

from sprocess import errors
from sprocess.scene import Scene


class TestScene(BaseTest):

    def test_scene_filenames_only(self):
        """ Test creation of Scene object with only filenames """
        images = Scene(self.files)
        imgs = images.open()
        self.assertTrue(isinstance(imgs, GeoImage))
        self.assertEqual(imgs.nbands(), len(self.files))

    def test_scene_filenames_and_bands(self):
        """ Test creation of Scene object with filenames and bands"""

        images = Scene(self.file_dict)
        images.open()
        self.assertTrue(images.is_open)
        self.assertEqual(images.geoimg.nbands(), len(self.file_dict))

    def test_scene_wrong_input(self):

        with self.assertRaises(Exception):
            Scene('path/to/file')

        with self.assertRaises(Exception):
            Scene({'path/to/file': 'red'})

    def test_scene_bands(self):
        scene = Scene(self.file_dict)

        # Get band names before opening the files
        with self.assertRaises(errors.SceneIsNotOpen):
            scene.bands

        # Get bands names after opening the files
        scene.open()
        bands = scene.bands
        self.assertTrue(isinstance(bands, tuple))
        self.assertEqual(len(bands), 10)

    def test_scene_basename(self):
        scene = Scene([self.files[0]])
        scene.open()
        self.assertEqual(scene.basename(), 'test_B1.tif')
