from .scene import Scene
from .product import NDVI, EVI, TrueColor


class Sentinel2(Scene, NDVI, EVI, TrueColor):
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

    def __init__(self, *args, **kwargs):
        super(Sentinel2, self).__init__(*args, **kwargs)

        filenames = self.filenames()
        for i, name in enumerate(filenames):
            band = self.get_bandname_from_file(name)
            if band:
                if band in self._bandmap.keys():
                    self.set_bandname(self._bandmap[band], i + 1)
                else:
                    self.set_bandname(band, i + 1)
