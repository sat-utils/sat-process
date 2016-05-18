import os
import re
from copy import copy

import rasterio
# import numpy as np
from errors import SatProcessError


class Raster(object):

    def __init__(self, raster, index, bandname):

        self.raster = raster
        self.index = index
        self.bandname = bandname
        self.np = None

    def __getattr__(self, name):
        return getattr(self.raster, name)

    def read(self):
        if self.np is None:
            self.np = self.raster.read(self.index)
        return self.np

    def write(self, arr):
        self.np = arr

    @property
    def filename(self):
        return self.raster.name

    @property
    def basename(self):
        return os.path.splitext(os.path.basename(self.filename))[0]


class Scene(object):
    """ Collection of bands for the same scene """

    def __init__(self, rasters, bandnames=[], *args, **kwargs):
        self.rasters = self._raster_factory(rasters, bandnames)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rasters[key]
        elif isinstance(key, str):
            try:
                band_index = self.bands.index(key)
                return self.rasters[band_index]
            except (IndexError, KeyError):
                raise SatProcessError('Invalid band name')
        else:
            raise SatProcessError('Invalid band number')

    def _raster_factory(self, rasters, bandnames):
        raster_array = []
        i = 0
        for r in rasters:
            bandname = self._generate_bandname(i, bandnames)

            if isinstance(r, Raster):
                new_raster = copy(r)
                new_raster.set_bandname = bandname
                raster_array.append(new_raster)
                i += 1
            else:
                # if the raster is a filename
                with rasterio.drivers():
                    src = rasterio.open(r, 'r')
                    for index in src.indexes:
                        new_raster = Raster(src, index, bandname)
                        raster_array.append(new_raster)
                        i += 1

        return raster_array

    def _generate_bandname(self, i, bandnames):
        try:
            return bandnames[i]
        except IndexError:
            return str(i + 1)

    def set_bandname(self, name, band_number):
        try:
            self.rasters[band_number - 1].bandname = name
        except IndexError:
            raise SatProcessError('The band number doesn\'t exist')

    def set_bandnames(self, names):

        if not isinstance(names, list):
            raise SatProcessError('Names must be a list')

        if len(names) != len(self.rasters):
            raise SatProcessError('Names should equal the number of bands')

        for i, name in enumerate(names):
            try:
                self.rasters[i].bandname = name
            except IndexError:
                raise SatProcessError('The band number doesn\'t exist')

        print(self.bands)

    def filenames(self):
        return [r.filename for r in self.rasters]

    def nbands(self):
        return len(self.rasters)

    def basename(self):
        return self.rasters[0].basename

    @property
    def bands(self):
        return [r.bandname for r in self.rasters]

    def bandnames(self):
        return self.bands

    @property
    def band_numbers(self):
        return self.nbands()

    def get_bandname_from_file(self, value):

        search = re.search('(B.{1,3})\.', value)
        if search:
            return search.group(0).replace('.', '')
        else:
            return None

    def save(self, path, dtype=None):
        """ Saves the first three rasters to the same file """

        rasterio_options = self.rasters[0].profile
        rasterio_options.update(
            count=3,
            photometric='RGB',
            nodata=0,
        )

        with rasterio.drivers():
            output = rasterio.open(path, 'w', **rasterio_options)

            for i in range(0, 3):
                output.write(self.rasters[i].read(), i + 1)

    def select(self, bands):
        """ Return instance of Scene instead of GeoImage """
        selection = []
        for band in bands:
            selection.append(self[band])

        return self.__class__(Scene(selection, self.bands))

    def has_bands(self, bands):
        for b in bands:
            if b not in self.bands:
                raise SatProcessError('Band %s is required' % b)
