from .scene import Scene
from .product import NDVI, TrueColor, ColorCorrection, SnowCoverage


class Landsat8(Scene, NDVI, TrueColor, ColorCorrection, SnowCoverage):
    description = 'Landsat Scene'

    # bandmap
    _bandmap = {
        1: 'coastal',
        2: 'blue',
        3: 'green',
        4: 'red',
        5: 'nir',
        6: 'swir1',
        7: 'swir2',
        8: 'pan',
        9: 'cirrus',
        'BQA': 'quality'
    }

    def __init__(self, *args, **kwargs):
        super(Landsat8, self).__init__(*args, **kwargs)

        filenames = self.filenames()
        for i, name in enumerate(filenames):
            band = self.get_bandname_from_file(name)
            if band:
                try:
                    bnum = [s for s in band if s.isdigit()]
                    band = int(''.join(bnum))
                except ValueError:
                    pass
                if band in self._bandmap.keys():
                    self.set_bandname(self._bandmap[band], i + 1)
                else:
                    self.set_bandname(band, i + 1)
