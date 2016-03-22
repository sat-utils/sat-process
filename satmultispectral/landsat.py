#!/usr/bin/env python

from scene import Scene


class LandsatScene(Scene):

    def SetMeta(self):
        """ Set metadata on scene """
        selg.geoimg.SetNoData(0)
        # read MTL and set data on self.geoimg
        # get gains/offsets for radiance, reflectance, etc.
        # get clouds, dynamic range
        # get geometry
