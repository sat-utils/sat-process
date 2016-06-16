
from .scene import Scene
from .product import TOA as _TOA, NDVI, EVI, Color


class TOA(_TOA):
    """ Base class for Sentinel2 products from original files """

    description = 'Sentinel2 TOA'

    dependencies = {}

    def open(self, *args, **kwargs):
        """ Open existing files to get TOA """
        super(TOA, self).open(*args, **kwargs)
        # set gain to convert to  reflectance units
        self.geoimg.set_gain(0.0001)
        return self.geoimg


class Sentinel2Scene(Scene):
    description = 'Sentinel2 Scene'

    _available_products = {
        'toa': TOA,
        'swir': TOA,
        'cbands': TOA,
        'ndvi': NDVI,
        'evi': EVI,
        'color': Color
    }

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

    _pattern = r'(.*)_(B.*).jp2'

    def __init__(self, *args, **kwargs):
        super(Sentinel2Scene, self).__init__(*args, **kwargs)
        # populate whatever products/bands available
        self.add_bands('toa', ['blue', 'green', 'red', 'nir'])
        self.add_bands('swir', ['swir1', 'swir2'])
        self.add_bands('cbands', ['coastal', 'cirrus'])
