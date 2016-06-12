from .scene import Scene
from .product import Product, DigitalCounts,  TOA as _TOA, NDVI, EVI, Color
from gippy import GeoImage


class TOA(_TOA):
    """ Top of the Atmosphere reflectance """

    def process(self, *args, **kwargs):
        """ Generate TOA from digital counts """
        super(TOA, self).process(*args, **kwargs)
        # TODO - set radiance gain and offset from metadata file
        if self.geoimg is None:
            geoimgs = self.get_dependencies()
            # convert from dc to reflectance
            self.geoimg = geoimgs[0]
        return self.geoimg


class Pan(Product):
    name = 'pan'
    description = 'High resolution panchromatic band'


class Radiance(Product):
    """ Apparent radiance """
    name = 'rad'
    description = 'Apparent radiance'

    dependencies = {'dc': []}

    def process(self, *args, **kwargs):
        """ Generate TOA from digital counts """
        super(Radiance, self).process(*args, **kwargs)
        # TODO - set radiance gain and offset from metadata file
        if self.geoimg is None:
            geoimgs = self.get_dependencies()
            # convert from dc to radiance
            self.geoimg = geoimgs[0]
        return self.geoimg


class Landsat8Scene(Scene):
    description = 'Landsat8 Scene'

    _available_products = {
        'quality': DigitalCounts,
        'dc': DigitalCounts,
        'pan': Pan,
        'rad': Radiance,
        'toa': TOA,
        'ndvi': NDVI,
        'evi': EVI,
        'color': Color
    }

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

    _pattern = r'(.*)_(B.*)\.(TIF|tif)'

    def __init__(self, *args, **kwargs):
        """ Open existing files as digital counts """
        super(Landsat8Scene, self).__init__(*args, **kwargs)
        # add pan product if present
        self.add_bands('pan', ['pan'])
        self.add_bands('quality', ['quality'])
        self.add_bands('dc', ['coastal', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'cirrus'])

