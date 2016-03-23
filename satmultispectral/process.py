#!/usr/bin/env python

import os
import gippy


class Process(object):
    """ Multispectral processing functions """

    def __init__(self, geoimg, outdir='./'):
        """ Initialize a Process instance """
        self.geoimg = geoimg
        self.output_prefix = os.path.join(outdir, geoimg.Basename())

    def ndvi(self):
        """ Calculate NDVI """
        # TODO - should filename be generated automatically?
        fout = self.output_prefix + '_ndvi'
        return gippy.Indices(self.geoimg, {'NDVI': fout})

    def pan(self, bands):
        """ Pansharpen bands with panchromatic band """
        print 'pansharpen'

    def color_correction(self, bands):
        """ Color stretch 3 bands to create 3 band image """
        print 'color_correction'
        return ''
