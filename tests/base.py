import re
import os
import glob
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self, path='samples/landsat8', extension='tif', scenes=None):

        self.test_dir = os.path.join(os.path.dirname(__file__), path)
        self.files = glob.glob(os.path.join(self.test_dir, '*.%s' % extension))

        if not scenes:
            self.scenes = {
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
        else:
            self.scenes = scenes

        print(self.scenes)
        print(self.files)

        self.file_dict = {}

        for f in self.files:
            search = re.search('(B.{1,3})\.', f)
            if search:
                band = search.group(0).replace('.', '')
                if band in self.scenes:
                    self.file_dict[f] = [self.scenes[band]]
