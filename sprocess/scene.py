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

    def __init__(self, raster=None, index=None, bandname=None, np_array=None, **kwargs):

        if not bandname:
            raise SatProcessError('You must provide bandname')

        self.bandname = bandname

        if raster:
            if not index:
                raise SatProcessError('You must provider index number for the Raster')

            self.raster = raster
            self.index = index
            self.name = raster.name
            self.crs = raster.crs
            self.affine = raster.affine
            self.width = raster.width
            self.height = raster.height
            self.dtype = raster.meta['dtype']
            self._profile = raster.profile
        else:
            if not isinstance(np_array, np.ndarray):
                raise SatProcessError('If the Raster class is not initialize from a Rasterio object ' +
                                      'then you must provide a numpy array')
            requried_kwargs = ['name', 'crs', 'affine', 'width', 'height', 'dtype', 'profile']
            for key in requried_kwargs:
                if key not in kwargs:
                    raise SatProcessError('%s is required when setting up a raster from numpy array' % key)
                setattr(self, key, kwargs[key])

        self.np = np_array
        self.reprojected = False

    @property
    def basename(self):
        return os.path.splitext(os.path.basename(self.filename))[0]

    @property
    def filename(self):
        return self.name

    @property
    def profile(self):
        self._profile.update(
            height=self.height,
            width=self.width,
            crs=self.crs,
            dtype=self.dtype
        )

        if self.reprojected:
            self._profile['transform'] = self.affine

        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    def read(self):
        if self.np is None:
            self.np = self.raster.read(self.index)
        return self.np

    def recast(self, dtype):
        try:
            self.np = convert(self.read(), getattr(np, dtype))
            self.dtype = dtype
        except AttributeError:
            raise SatProcessError('data type %s is invalid' % dtype)

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

    def _generate_bandname(self, i, bandnames):
        try:
            return bandnames[i]
        except IndexError:
            return str(i + 1)

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

    def add(self, raster):
        """ adds a raster to the scene """
        if not isinstance(raster, Raster):
            raise SatProcessError('raster must be of type Raster')
        self.rasters.append(raster)

        return self

    @property
    def bands(self):
        return [r.bandname for r in self.rasters]

    def bandnames(self):
        return self.bands

    @property
    def band_numbers(self):
        return self.nbands()

    def basename(self):
        return self.rasters[0].basename

    def delete(self, keys):
        """ Remove raster from the scene """

        if not isinstance(keys, list):
            raise SatProcessError('Keys must be a python list')

        for key in keys:
            if isinstance(key, int):
                del self.rasters[key]
            elif isinstance(key, str):
                index = self.bands.index(key)
                del self.rasters[index]

    def filenames(self):
        return [r.filename for r in self.rasters]

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

    def nbands(self):
        return len(self.rasters)

    def recast(self, dtype):
        for raster in self.rasters:
            raster.recast(dtype)

        return self

    def reproject(self, dst_crs):
        for r in self.rasters:
            r.reproject(dst_crs)

        return self

    def save(self, path, driver='GTiff', colormap=None, bands=None):
        """ Saves the first three rasters to the same file """

        if not path:
            raise SatProcessError('Path must be provided')

        # get image data from the first raster
        raster = self.rasters[0]

        if bands and isinstance(bands, list) and len(bands) < 4:
            count = len(bands)
            iterator = bands
        else:
            count = self.nbands() if self.nbands() < 3 else 3
            iterator = range(0, count)

        rasterio_options = raster.profile
        rasterio_options.update(
            count=count,
            driver=driver,
        )

        if count == 3:
            rasterio_options['photometric'] = 'RGB'

        with rasterio.drivers():
            output = rasterio.open(path, 'w', **rasterio_options)

            for i, key in enumerate(iterator):
                band = self[key].read()
                output.write(band, i + 1)

                if colormap:
                    output.write_colormap(i + 1, colormap)

    def select(self, bands):
        """ Return instance of Scene instead of GeoImage """
        selection = []
        for band in bands:
            selection.append(self[band])

        return self.__class__(Scene(selection, self.bands))

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
