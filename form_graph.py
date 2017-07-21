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

    def __init__(self, emitters=None, middles=None, detectors=None, radius=50e-9, index_refraction= 1 + 2.67150153E-3):
        super(FormGraph, self).__init__(title="Form Factor of Sphere with Curved Paths",
                                        bottom="Q Value", left="Probability Density")
        self.index_refraction = index_refraction
        self.sphere_radius = radius

        num_points = 1
        length = ((num_points * 2) - 1) * 100e-9

        # print([[[0, 0, ((-length/2 + radius) + 4 * n * radius)], self.sphere_radius, index_refraction] for n in range(num_points)])

        # initialize emitters
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        pd1, qz1, qx1 = calc_norm((0, 6e-8), (1, 100), (0, 2), (1, 20000), [[[0, 0, 0], 3e-8, 0]])
        pd2, qz2, qx2 = calc_norm((0, 6e-8), (1, 1000), (0, 2), (1, 20000), [[[0, 0, 0], 3e-8, 0]])
        # pd3, qz3, qx3 = calc_norm((0, 6e-8), (1, 10000), (0, 2), (1, 20000), [[[0, 0, 0], 3e-8, 0]])
        # pd4, qz4, qx4 = calc_norm((0, 6e-8), (1, 100000), (0, 2), (1, 20000), [[[0, 0, 0], 3e-8, 0]])
        self.plot(qz1, FormGraph.scale(pd1), connect='all', pen="r")
        self.plot(qz2, FormGraph.scale(pd2), connect='all', pen="b")
        # self.plot(qz3, FormGraph.scale(pd3), connect='all', pen="g")
        # self.plot(qz4, FormGraph.scale(pd4), connect='all', pen="y")

        # pd2, qz2, qx2 = calc_norm((1, length), (1, 700), (1, 20), (1, 20000), [[[0, 0, 0], radius, 0]])
        # self.plot(qz2, pd2, connect='all', pen="b")

        # pd3 = (np.array(pd1) - np.array(pd2)).tolist()
        # self.plot(qz2, pd3, symbol="o", symbolPen="#000000", symbolBrush="g", symbolSize=4, connect='all', pen="g")
    @staticmethod
    def scale(array):
        """ Normalizes variables in an array to between 0 and 1 by manipulating them based on the min and max functions """
        if isinstance(array, list):
            array = np.array(array)
        min_ = min(array)
        divisor = max(array) - min_
        if divisor == 0:
            print("Saved")
            return np.ones(array.shape)
        return (array - min_) / divisor
