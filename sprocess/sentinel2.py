
from .scene import Scene
from gippy import GeoImage
from .product import Product, NDVI, EVI, Color


class Sentinel2Product(Product):
    """ Base class for Sentinel2 products from original files """

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

    def open(self, filenames, **kwargs):
        """ Open existing files to get TOA """
        # open products
        bandnames = [self.parse_filename(f)[1] for f in filenames]
        self.geoimg = GeoImage.open(filenames, bandnames=bandnames, gain=0.0001)
        return self.geoimg


class TOA(Sentinel2Product):
    """ Top of the atmosphere reflectance product optical for Sentinel2 """
    # Note that this only works with the 4 10m bands: 2, 3, 4, and 8

    name = 'toa'
    description = 'Top of the Atmosphere reflectance'


class Sentinel2Scene(Scene):
    description = 'Sentinel2 Scene'

    _available_products = [
        TOA,
        NDVI,
        EVI,
        Color
    ]

    default_product = 'toa'
