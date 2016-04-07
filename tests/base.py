import os
import glob
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):

        self.test_dir = os.path.join(os.path.dirname(__file__), 'samples/landsat8')
        self.files = glob.glob(os.path.join(self.test_dir, '*.tif'))

        self.landsat8 = {
            'B1': 'coastal',
            'B2': 'blue',
            'B3': 'green',
            'B4': 'red',
            'B5': 'nir',
            'B6': 'swir1',
            'B7': 'swir2',
            'B8': 'pan',
            'B9': 'cirrus',
            'BQA': 'quality'
        }

        self.file_dict = {}

        for f in self.files:
            band = f.split('_')[-1].split('.')[0]
            if band in self.landsat8:
                self.file_dict[f] = [self.landsat8[band]]
