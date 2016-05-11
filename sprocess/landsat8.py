from .scene import Scene
from .product import NDVI, TrueColor


class Landsat8(Scene, NDVI, TrueColor):
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

    def __init__(self, *args, **kwargs):
        super(Landsat8, self).__init__(*args, **kwargs)

        filenames = self.filenames()
        for i, name in enumerate(filenames):
            band = self.get_bandname_from_file(name)
            if band:
                if band in self._bandmap.keys():
                    self.set_bandname(self._bandmap[band], i + 1)
                else:
                    self.set_bandname(band, i + 1)
