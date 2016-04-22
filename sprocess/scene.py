import re
import gippy


class Scene(gippy.GeoImage):
    """ Collection of bands for the same scene """

    @property
    def bands(self):
        return self.bandnames()

    @property
    def band_numbers(self):
        return self.nbands()

    def get_bandname_from_file(self, value):

        # print(value)
        search = re.search('(B.{1,3})\.', value)
        if search:
            return search.group(0).replace('.', '')
        else:
            return None
