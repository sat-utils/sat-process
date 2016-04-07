from six import iteritems

from .scene import Scene
from .product import NDVI, EVI
from .errors import SatProcessError


# Landsat specific Products
class Sentinel2(Scene, NDVI, EVI):
    description = 'Landsat Scene'

    # bandmap
    _bandmap = {
        'B01': 'coastal',
        'B02': 'blue',
        'B03': 'green',
        'B04': 'red',
        'B08': 'nir',
        'B10': 'cirrus',
        'B11': 'swir1',
        'B12': 'swir2'
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

        super(Sentinel2, self).__init__(filenames)
