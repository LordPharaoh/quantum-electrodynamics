from __future__ import division
import pyqtgraph as pg
import resource
import numpy as np
from random import uniform
from geometry import Point
from c_ext.calc_norm import calc_norm
from pipeline import msg
from xicam import threads
import warnings

class FormGraph(pg.PlotWidget):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=50e-9, index_refraction= 1 - 2.67150153E-6):
        super(FormGraph, self).__init__(title="Form Factor of Sphere with Curved Paths",
                                        bottom="Q Value", left="Probability Density")
        self.index_refraction = index_refraction
        self.sphere_radius = radius

        num_points = 1
        length = ((num_points * 2) - 1) * 100e-9

        # print([[[0, 0, ((-length/2 + radius) + 4 * n * radius)], self.sphere_radius, index_refraction] for n in range(num_points)])

        # initialize emitters

        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        middles = [1e3, 1e4]
        for idx, mid in enumerate(middles):
            pd1, qz1, qx1 = calc_norm((0, 6e-8), (1, mid), (0, 10), (1, 1000), [[[0, 0, 1e-10], 3e-8, 1]])
            self.plot(qz1, FormGraph.scale(pd1), connect='all', pen=pg.mkPen(((255 / len(middles)) * idx, 0, 255 - ((255 / len(middles)) * idx))))

    @staticmethod
    def scale(array):
        """ Normalizes variables in an array to between 0 and 1 by manipulating them based on the min and max functions """
        if isinstance(array, list):
            array = np.array(array)
        min_ = 0
        divisor = max(array) - min_
        if divisor == 0:
            return np.ones(array.shape)
        return (array - min_) / divisor
