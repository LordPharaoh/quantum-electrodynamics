from __future__ import division
import pyqtgraph.opengl as gl
from c_ext.calc_norm import calc_norm
from random import uniform
from geometry import Point
from glitems import Arc, Sphere, Scatter
import numpy as np
from pipeline import msg


class Main3DView(gl.GLViewWidget):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=6, index_refraction=.2):

        super(Main3DView, self).__init__()
        self.addItem(gl.GLAxisItem())
        self.index_refraction = index_refraction
        self.sphere_radius = radius

        # Draw sphere first so it goes under everything else
        self.addItem(Sphere(Point(0, 0, 0), self.sphere_radius))
