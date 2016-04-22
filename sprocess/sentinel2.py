from .scene import Scene
from .product import NDVI, EVI


class Sentinel2(Scene, NDVI, EVI):
    description = 'Landsat Scene'

    # bandmap
    bands_map = {
        'B01': 'coastal',
        'B02': 'blue',
        'B03': 'green',
        'B04': 'red',
        'B08': 'nir',
        'B10': 'cirrus',
        'B11': 'swir1',
        'B12': 'swir2'
    }
