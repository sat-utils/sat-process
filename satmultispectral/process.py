#!/usr/bin/env python

import gippy


class Process(object):
    """ Multispectral processing functions """

    @staticmethod
    def ndvi(geoimg, fout):
        """ Calculate NDVI """
        return gippy.Indices(geoimg, {'NDVI': fout})

    @staticmethod
    def pan(geoimg, fout, bands):
        """ Pansharpen bands with panchromatic band """
        print 'pansharpen'

    @staticmethod
    def color_correction(geoimg, fout, bands):
        """ Color stretch 3 bands to create 3 band image """
        print 'color_correction'
        return fout
