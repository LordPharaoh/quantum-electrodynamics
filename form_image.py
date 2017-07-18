from __future__ import division
import pyqtgraph as pg
from random import uniform
from geometry import Point, Circle
import sys
import numpy as np
from c_ext.calc_norm import calc_norm
from pipeline import msg
from xicam import threads
import math


class FormImage(pg.ImageView):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=5E-8, index_refraction=1 - 2.67150153E-6):
        super(FormImage, self).__init__()
        self.index_refraction = index_refraction
        IM_SIZE = 200
        Q_RANGE = 20
        self.sphere_radius = radius
        self.probability_density, self.qz_values, self.qx_values = calc_norm((300e-9, 300e-9), (100, 100), (Q_RANGE, Q_RANGE), (IM_SIZE - 1, IM_SIZE - 1), 
                                             [[[100e-9, 0, 0], self.sphere_radius, self.index_refraction], [[-100e-9, 0, 0], self.sphere_radius, self.index_refraction]])


        self.imarray = np.zeros((IM_SIZE, IM_SIZE), dtype=float);

        #scale q values to 200x200
        self.qz_values = np.trunc(np.array(self.qz_values) * (IM_SIZE / Q_RANGE))
        self.qx_values = np.trunc(np.array(self.qx_values) * (IM_SIZE / Q_RANGE))
        self.probability_density = FormImage.scale(np.array(self.probability_density))

        for qz, qx, pd in zip(self.qz_values, self.qx_values, self.probability_density):
            try:
                self.imarray[int(round(qx)), int(round(qz))] = pd
            except ValueError:
                print("failed at setting ({}, {}) to {}".format(qx, qz, pd))

        self.setImage(self.imarray)

    @staticmethod
    def scale(array):
        """ Normalizes variables in an array to between 0 and 1 by manipulating them based on the min and max functions """
        min_ = min(array)
        divisor = max(array) - min_
        if divisor == 0:
            print("Saved")
            return np.ones(array.shape)
        return (array - min_) / divisor

