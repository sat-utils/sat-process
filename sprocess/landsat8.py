from .scene import Scene
from .product import Product, DigitalCounts as _DigitalCounts, TOA as _TOA, NDVI, EVI, Color
from gippy import GeoImage


class DigitalCounts(_DigitalCounts):

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

    #_pattern = r'(.*)_(B.*).TIF'

    def open(self, filenames, **kwargs):
        """ Open existing files as digital counts """
        # open products
        bandnames = [self.parse_filename(f)[1] for f in filenames]
        self.geoimg = GeoImage.open(filenames, bandnames=bandnames)
        return self.geoimg


class TOA(_TOA):
    """ Top of the Atmosphere reflectance """

    def process(self, filename=None, **kwargs):
        """ Generate TOA from digital counts """
        geoimg = self.scene.dc()
        # TODO - set radiance gain and offset from metadata file
        return geoimg


class Radiance(Product):
    """ Apparent radiance """
    name = 'rad'
    description = 'Apparent radiance'

    def process(self, filename=None, **kwargs):
        """ Generate TOA from digital counts """
        geoimg = self.scene.dc()
        # TODO - set TOA gain and offset from metadata file
        return geoimg


class Landsat8Scene(Scene):
    description = 'Landsat8 Scene'

    _available_products = [
        DigitalCounts,
        TOA,
        NDVI,
        EVI,
        Color
    ]


