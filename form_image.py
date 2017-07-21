from __future__ import division
import pyqtgraph as pg
from random import uniform
from geometry import Point, Circle
import resource
import sys
import numpy as np
from c_ext.calc_norm import calc_norm
from pipeline import msg
from xicam import threads
import math


class FormImage(pg.ImageView):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=50E-9, index_refraction=1 - 2.67150153E-6):
        super(FormImage, self).__init__()
        self.index_refraction = index_refraction
        IM_SIZE = 50
        Q_RANGE = 30

        self.sphere_radius = radius
        num_points = 10
        length = ((num_points * 2) - 1) * 100e-9

        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        self.probability_density, self.qz_values, self.qx_values = calc_norm((1, 6 * self.sphere_radius), (400, 400), (Q_RANGE, Q_RANGE), (IM_SIZE, IM_SIZE), [[[0, 0, ((-length/2 + radius) + 4 * n * radius)], self.sphere_radius, index_refraction] for n in range(num_points)])

        #scale q values to 200x200
        self.qz_values = (FormImage.scale(np.array(self.qz_values)) * IM_SIZE).astype(int)
        self.qx_values = (FormImage.scale(np.array(self.qx_values)) * IM_SIZE).astype(int)
        self.probability_density = FormImage.scale(np.array(self.probability_density))

        print(min(self.qz_values))
        print(min(self.qx_values))

        self.imarray = np.zeros((IM_SIZE + 1, IM_SIZE + 1), dtype=float);

        for qz, qx, pd in zip(self.qz_values, self.qx_values, self.probability_density):
            try:
                self.imarray[qx, qz] = pd
            except ValueError, IndexError:
                print("failed at setting ({}, {}) to {}".format(qx, qz, pd))

        # this method of delete is sketch but there should just be one black row so it should be ok I think?
        self.imarray = np.vstack((np.flipud(self.imarray), self.imarray))
        self.imarray = np.hstack((np.fliplr(self.imarray), self.imarray))
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
