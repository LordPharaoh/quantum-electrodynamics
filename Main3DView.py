from __future__ import division
import pyqtgraph.opengl as gl
from calc_norm import calc_norm
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

        # initialize emitters
        if emitters is None:
            self.emitters = [Point(0, -1000, 0)]
        else:
            self.emitters = emitters
        if middles is None:
            self.middles = [Point(uniform(-4, 4), 0, uniform(-4, 4)) for i in range(10)]
        else:
            self.middles = middles
        if detectors is None:
            self.detectors = [Point(uniform(-4, 4), 10, uniform(-4, 4)) for i in range(10)]
        else:
            self.detectors = detectors

        # calculate and sum times for each path
        self.norms = calc_norm(self.emitters, self.middles, self.detectors, self.sphere_radius,
                               self.index_refraction)[0]

        # rescaling evenly with stddev to spread out
        # this assumes they're gaussian and spreads them out constantly. They're probably not gaussian, but it should
        # spread the values out somewhat anyway
        self.stddev_norm = np.std(self.norms)
        self.mean_norm = np.mean(self.norms)
        self.norms = list(map(lambda t: (t - self.mean_norm) / self.stddev_norm, self.norms))
        msg.logMessage(self.norms)

        # Scale all values between 0 and 1
        self.max_norm = max(self.norms)
        self.min_norm = min(self.norms)
        self.norms = list(map(lambda t: (t - self.min_norm) / (self.max_norm - self.min_norm), self.norms))

        # Draw arcs
        idx = 0
        for e in self.emitters:
            for m in self.middles:
                for d in self.detectors:
                    t = self.norms[idx]
                    color = (t, 1 - t, 0, .2)
                    msg.logMessage(color)
                    self.addItem(Arc(e, m, d, color))
                    idx += 1

        # Draw keypoints
        self.addItem(Scatter(np.array(self.emitters + self.middles + self.detectors)))

