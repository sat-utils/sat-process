import gippy


class Scene(gippy.GeoImage):
    """ Collection of bands for the same scene """

    @property
    def bands(self):
        return self.bandnames()

    @property
    def band_numbers(self):
        return self.nbands()
