#!/usr/bin/env python

import os
import re
import gippy
import gippy.algorithms as algs

"""
    Product classes which represent files on disk and processing required
"""

# example band descriptions
_band_descriptions = {
    'coastal':  'Coastal band (~0.43um)',
    'pan':      'Panchromatic band',
    'blue':     'Blue band',
    'green':    'Green band',
    'red':      'Red band',
    'nir':      'Near IR band',
    'cirrus':   'Cirrus cloud detection band (~1.38um)',
    'swir1':    'Shortwave IR band (~1.65um)',
    'swir2':    'Shortwave IR band (~2.2um)',
    'quality':  'quality metric'
}


class ImageFiles(object):
    """ Collection of image files """

    # dictionary of , currently assumes different files
    filenames = {}

    def __init__(self, filenames, bandnames=None):
        """ Create collection of bands from {bandname; filename} dict """
        if bandnames is not None:
            if bandnames[0] == '':
                bandnames = None
        self.bandnames = bandnames
        self.filenames = filenames

    def open(self):
        """ Open filenames as a GeoImage with bandnames """
        if len(self.filenames) == 1:
            fnames = self.filenames[0]
        else:
            fnames = self.filenames
        geoimg = gippy.GeoImage(fnames)
        if self.bandnames is not None:
            nb = max(geoimg.NumBands(), len(self.bandnames))
            for i in range(0, nb):
                geoimg.SetBandName(self.bandnames[i], i+1)
        # else assume bandnames are set in file metadata
        return geoimg


class Product(object):
    """ A Product is some input (either files, or another series of Products)
        and some processing performed on that input. """

    description = 'Product Base Class'

    # dependencies in the form {product: [bands]}
    dependencies = {}

    # map of original band names to common bandnames
    _bandmap = {}

    def __init__(self, input_products=None, filenames=None):
        """ Create a new output product from input product """
        self.files = filenames
        if filenames is not None:
            # get lists from filenames
            bandnames = sorted(filenames.keys())
            filenames = [filenames[f] for f in sorted(filenames.keys())]
            self.files = ImageFiles(filenames, bandnames)
        self.input_products = input_products
        if self.files is None and self.input_products is None:
            raise Exception('cannot create a product from nothing')

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def pattern(cls):
        """ Regular expression for matching product files with 2 groups: basename and product/band """
        return r'(.*)_(%s.*)' % (cls.name())

    def process(self, outfile=None, outpath='./', overwrite=False):
        """ Perform processing on input product and return output GeoImage """
        if overwrite and self.input_products is not None:
            self.files = None
        if self.files is not None:
            # if files already exist just return those
            geoimg = self.files.open()
        else:
            # get first input product. child classes must
            # retrieve others (if any) themselves!
            geoimg = self.input_products[0].process()
        # if outfile is not supplied, generate name based on input image basename
        if outfile is None:
            outfile = os.path.join(outpath, geoimg.Basename() + '_' + self.name())
        # name of output file (when processed), for the benefit of child
        # classes calling this function via super()
        self.outfile = outfile

        return geoimg

    def save(self, geoimg, outfile=None, outpath='./', overwrite=False):
        """ Save geoimg to file and add filenames to instance """
        # reset to force save anyway
        if overwrite and self.input_products is not None:
            self.files = None
        if self.files is None:
            # create an output filename if not provided
            if outfile is None:
                outfile = os.path.join(outpath, geoimg.Basename() + '_' + self.name())
            geoimg.save(outfile)
            self.files = ImageFiles({'': outfile})

    def add_parser(self, parser):
        """ Add options for this product to this command line parser """
        parser.add_argument('--%s' % self.name(), help=self.description, default=False, action='store_true')

    @classmethod
    def parse_filename(cls, filename):
        """ Parse filename for basename and bandname (remapped if _bandmap) """
        m = re.match(cls.pattern(), os.path.basename(filename))
        basename = m.group(1)
        bandname = cls._bandmap.get(m.group(2), m.group(2))
        return basename, bandname

    @classmethod
    def create_from_filenames(cls, filenames):
        """ Parse filenames for any matching this product """
        filenames2 = [f for f in filenames if re.match(cls.pattern(), os.path.basename(f))]
        if len(filenames2) > 1:
            # extract bandnames ('_suffix' of filename, no extension)
            bandnames = [cls.parse_filename(b)[1] for b in filenames2]
            return cls(filenames=dict(zip(bandnames, filenames2)))
        elif len(filenames2) == 1:
            # product in single file (most common outside of original files)
            return cls(filenames={'': filenames2[0]})
        else:
            return None


class DC(Product):
    """ Digital counts from sensor """
    description = 'Digital counts'


class TOA(Product):
    """ Top of the Atmosphere reflectance """
    description = 'Top of the Atmosphere (TOA) Reflectance'
    dependencies = {
        'dc': []
    }

    def process(self, **kwargs):
        geoimg = super(TOA, self).process(**kwargs)
        # set gain and offsets to bring to reflectance
        return geoimg


class NDVI(Product):
    description = 'Normalized Difference Vegetation Index (NDVI) from TOA reflectance'
    dependencies = {
        'toa': ['nir', 'red']
    }

    def process(self, **kwargs):
        geoimg = super(NDVI, self).process(**kwargs)
        prods = {'ndvi': self.outfile}
        fouts = algs.Indices(geoimg, prods)
        # add the single filename
        # TODO - improve this whole single file vs multiple file fiasco
        self.files = ImageFiles(fouts.values()[0])
        return self.files.open()


class Color(Product):
    """ Stretch 3 input bands to create 3 band color image """

    description = 'Stretch 3 input bands to create 3band color image'

    dependencies = {
        'dc': []
    }

    def process(self, **kwargs):
        """ Process data into output product """
        geoimg = super(Color, self).process(**kwargs)
        geoimg = self.input_product.open()
        return geoimg


class PanSharpen(Product):
    description = 'Sharpen bands with higher resolution panchromatic band'

    def process(self):
        pass
        # geoimage will need to return higher resolution band separately?
