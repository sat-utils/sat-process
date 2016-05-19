import os
import re
from copy import copy

import rasterio
import numpy as np
from rasterio import crs
from rasterio.warp import calculate_default_transform, reproject, RESAMPLING
from errors import SatProcessError
from converter import convert


class Raster(object):

    def __init__(self, raster, index, bandname):

        self.raster = raster
        self.index = index
        self.bandname = bandname
        self.np = None
        self.crs = raster.crs
        self.affine = raster.affine
        self.width = raster.width
        self.height = raster.height

        self.reprojected = False

    def __getattr__(self, name):
        return getattr(self.raster, name)

    @property
    def basename(self):
        return os.path.splitext(os.path.basename(self.filename))[0]

    @property
    def filename(self):
        return self.raster.name

    @property
    def profile(self):
        _profile = self.raster.profile

        _profile.update(
            height=self.height,
            width=self.width,
            crs=self.crs
        )

        if self.reprojected:
            _profile['transform'] = self.affine

        return _profile

    def read(self):
        if self.np is None:
            self.np = self.raster.read(self.index)
        return self.np

    def reproject(self, dst_crs):
        # if the image is geotiff, use rasterio's helper

        dst_crs = crs.from_string(dst_crs)

        affine, width, height = calculate_default_transform(
            self.crs, dst_crs, self.width, self.height, *self.bounds
        )

        dst = np.zeros((height, width), getattr(np, self.meta['dtype']))

        reproject(
            source=self.read(),
            destination=dst,
            src_transform=self.affine,
            src_crs=self.crs,
            dst_transform=affine,
            dst_crs=dst_crs,
            resampling=RESAMPLING.nearest,
            num_threads=4
        )

        self.np = dst

        # record new dimensions
        self.crs = dst_crs
        self.height = height
        self.width = width
        self.affine = affine
        self.reprojected = True

    def write(self, arr):
        self.np = arr


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

    def has_bands(self, bands):
        for b in bands:
            if b not in self.bands:
                raise SatProcessError('Band %s is required' % b)

    def reproject(self, dst_crs):
        for r in self.rasters:
            r.reproject(dst_crs)

    def save(self, path, dtype=None):
        """ Saves the first three rasters to the same file """

        # get image data from the first raster
        raster = self.rasters[0]

        rasterio_options = raster.profile
        rasterio_options.update(
            count=3,
            photometric='RGB',
        )

        if dtype:
            rasterio_options['dtype'] = dtype

        with rasterio.drivers():
            output = rasterio.open(path, 'w', **rasterio_options)

            for i in range(0, 3):
                band = self.rasters[i].read()

                if dtype:
                    band = convert(band, getattr(np, dtype))
                output.write(band, i + 1)

    def select(self, bands):
        """ Return instance of Scene instead of GeoImage """
        selection = []
        for band in bands:
            selection.append(self[band])

        return self.__class__(Scene(selection, self.bands))
