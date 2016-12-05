from .scene import Scene
from .product import NDVI, NBR, TrueColor, ColorCorrection


class Sentinel2(Scene, NDVI, NBR, TrueColor, ColorCorrection):
    description = 'Landsat Scene'

    # bandmap
    _bandmap = {
        1: 'coastal',
        2: 'blue',
        3: 'green',
        4: 'red',
        8: 'nir',
        10: 'cirrus',
        11: 'swir1',
        12: 'swir2'
    }

    def __init__(self, *args, **kwargs):
        super(Sentinel2, self).__init__(*args, **kwargs)

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
