import os
import gippy
from six import iteritems, itervalues

from .errors import SceneIsNotOpen, SatProcessError


def scene_open_check(func):
    def check(self, *args, **kwargs):
        if not self.is_open:
            raise SceneIsNotOpen

        return func(self, *args, **kwargs)
    return check


class Scene(object):
    """ Collection of bands for the same scene """

    band_descriptions = {
        'coastal': 'Coastal band (~0.43um)',
        'pan': 'Panchromatic band',
        'blue': 'Blue band',
        'green': 'Green band',
        'red': 'Red band',
        'nir': 'Near IR band',
        'cirrus': 'Cirrus cloud detection band (~1.38um)',
        'swir1': 'Shortwave IR band (~1.65um)',
        'swir2': 'Shortwave IR band (~2.2um)',
        'quality': 'quality metric'
    }

    def __init__(self, filenames):
        """ Creates gippy GeoImage from the filenames provided.
        filenames could be a list or a dictionary. A list should include the path to every image.
        A dictionary should have the filepath as key and a list of bands as value.
        list of bands should be in the order the bands are saved in the file.
        Make sure to use band names instead of numbers

        Example:

        scene1 = Scene(['path/to/file1.tif', 'path/to/file2.tif', 'path/to/file3.tif'])
        scene2 = Scene({
            'path/to/file1.tif': ['red', 'green', 'blue'],
            'path/to/file2.tif': ['green']
        })

        image1.open()
        image2.open()

        """
        self.only_files = None
        self.file_bands = None

        if not filenames:
            raise SatProcessError('Filenames are missing')

        if isinstance(filenames, list):
            self.only_files = filenames

        elif isinstance(filenames, dict):
            for bands in itervalues(filenames):
                if not isinstance(bands, list):
                    raise SatProcessError('bands must be list')
            self.file_bands = filenames
        else:
            raise SatProcessError('Filenames must be a list or a dictionary')

        self.geoimg = None

    @scene_open_check
    def basename(self):
        return os.path.basename(self.geoimg.Filename())

    @property
    @scene_open_check
    def bands(self):
        return self.geoimg.BandNames()

    @property
    @scene_open_check
    def band_numbers(self):
        return self.geoimg.NumBands()

    @property
    def is_open(self):
        if self.geoimg:
            return True
        else:
            return False

    def open(self):
        """ Open filenames as a GeoImage with bandnames """

        if self.only_files:
            self.geoimg = gippy.GeoImage(self.only_files)
            return self.geoimg
        elif self.file_bands:
            # making sure the filenames and bands are in the right order
            # for example if the first file has one band, the second file has 3 bands
            # the third file has 2 bands, iteration below ensures everything are
            # in the right order
            filenames = []
            bands = []
            for f, bs in iteritems(self.file_bands):
                filenames.append(f)
                bands.extend(bs)

            self.geoimg = gippy.GeoImage(filenames)
            for i, band in enumerate(bands):
                self.geoimg.SetBandName(band, i + 1)

            return self
        else:
            raise SatProcessError('Unexpected error!')

    @scene_open_check
    def save(self, path):
        """ Save geoimg to file and add filenames to instance """
        self.geoimg.save(path)
