import pyqtgraph as pg
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

        num_points = 10
        length = ((num_points * 2) - 1) * 100e-9

        print([[[0, 0, ((-length/2 + radius) + 4 * n * radius)], self.sphere_radius, index_refraction] for n in range(num_points)])

        # initialize emitters
        pd1, qz1, qx1 = calc_norm((0, length), (1, 700), (0, 10), (1, 20000), [[[0, 0, ((-length/2 + radius) + 4 * n * radius)], self.sphere_radius, index_refraction] for n in range(num_points)])
        self.plot(qz1, pd1, symbol="o", symbolPen="#000000", symbolBrush="r", symbolSize=4, connect='all', pen="r")

        pd2, qz2, qx2 = calc_norm((0, length), (1, 700), (0, 10), (1, 20000), [[[0, 0, 0], self.sphere_radius, index_refraction]])
        self.plot(qz2, pd2, symbol="o", symbolPen="#000000", symbolBrush="b", symbolSize=4, connect='all', pen="b")

        pd3 = (np.array(pd1) - np.array(pd2)).tolist()
        self.plot(qz2, pd3, symbol="o", symbolPen="#000000", symbolBrush="g", symbolSize=4, connect='all', pen="g")
