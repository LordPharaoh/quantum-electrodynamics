from __future__ import division
import pyqtgraph.opengl as gl
from calc_times import calc_times
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
            self.emitters = [Point(0, -10, 0)]
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
        self.times = list(map(sum, calc_times(self.emitters, self.middles, self.detectors, self.sphere_radius,
                                         self.index_refraction)))
        msg.logMessage(self.times)

        # rescaling values to stddev between 1 and 0
        self.stddev_time = np.std(self.times)
        self.mean_time = np.mean(self.times)
        self.times = list(map(lambda t: (t - self.mean_time) / self.stddev_time, self.times))
        msg.logMessage(self.times)

        self.max_time = max(self.times)
        self.min_time = min(self.times)
        self.times = list(map(lambda t: (t - self.min_time) / (self.max_time - self.min_time), self.times))
        msg.logMessage(self.times)

        # Draw arcs
        idx = 0
        for e in self.emitters:
            for m in self.middles:
                for d in self.detectors:
                    t = self.times[idx]
                    color = (t, 1 - t, 0, .2)
                    msg.logMessage(color)
                    self.addItem(Arc(e, m, d, color))
                    idx += 1


        # Draw keypoints
        self.addItem(Scatter(np.array(self.emitters + self.middles + self.detectors)))

