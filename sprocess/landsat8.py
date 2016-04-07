from six import iteritems

from .scene import Scene
from .product import NDVI, EVI
from .errors import SatProcessError


# Landsat specific Products
class Landsat8(Scene, NDVI, EVI):
    description = 'Landsat Scene'

    # bandmap
    _bandmap = {
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

    def __init__(self, filenames):

        if not isinstance(filenames, dict):
            raise SatProcessError('Both filename and band name must be provided for landsat scenes. ' +
                                  'You can either use landsat band numbers or descriptive names e.g. red')
        # replace landsat band numbers with bandmap names
        for f, bands in iteritems(filenames):
            for i, band in enumerate(bands):
                if band.upper() in self._bandmap:
                    bands[i] = self._bandmap[band.upper()]

            filenames[f] = bands

        super(Landsat8, self).__init__(filenames)
