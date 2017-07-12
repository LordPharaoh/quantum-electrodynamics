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
        self.sphere_radius = radius

        IM_SIZE = 200

        # initialize emitters
        if emitters is None:
            self.emitters = [Point(0, -16, 0)]
        else:
            self.emitters = emitters
        if middles is None:
            self.sphere_radius = 4 * self.sphere_radius
            self.middles = self.sphere(900)
        else:
            self.middles = middles
        if detectors is None:
            r = 1E-0
            npt = IM_SIZE
            self.detectors = []
            for i in range(1, npt):
                for j in range(1, npt):
                    self.detectors.append(Point((r/npt) * (i - npt / 2), 4, (r/npt) * (j - npt / 2)))
        else:
            self.detectors = detectors


        self.probability_density, self.qz_values, self.qx_values = calc_norm(self.emitters, self.middles, self.detectors,
                                                                             self.sphere_radius, self.index_refraction)

        print(max(self.qz_values))
        print(max(self.qx_values))
        print(min(self.qz_values))
        print(min(self.qx_values))

        self.imarray = np.zeros((IM_SIZE, IM_SIZE), dtype=float);

        #scale q values to 200x200
        self.qz_values = FormImage.scale(np.array(self.qz_values)) * (IM_SIZE - 1)
        self.qx_values = FormImage.scale(np.array(self.qx_values)) * (IM_SIZE - 1)
        self.probability_density = FormImage.scale(np.array(self.probability_density))

        for qz, qx, pd in zip(self.qz_values, self.qx_values, self.probability_density):
            try:
                self.imarray[int(qx), int(qz)] = pd
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

    def sphere(self, num_points):
        """ Creates a sunflower seed spiral pattern which evenly distributes points along a plane """
        points = []
        phi = (math.sqrt(5) + 1) / 2
        for k in range(1, num_points):
            r = math.sqrt(k - .5) / math.sqrt(num_points - .5) * (self.sphere_radius - 1E-15)
            theta = 2 * np.pi * k / phi ** 2
            points.append(Point(r * np.cos(theta), 1E-20, r * np.sin(theta)))

        return points

    def cube(self, n_points):
        """ Generates a cube with sides self.radius * 2 """
        n_points = int(sqrt(n_points))
        step = self.sphere_radius / n_points
        for x in range(n_points):
            for z in range(n_points):
                self.middles.append(Point((x - n_points/2) * step, 1E-20, (z - n_points/2) * step))

    def cylinder(self, n_points, zangle, xangle):
        """ 
        Finds equation of ellipse which goes down a cylinder
        zangle is the nalge which affects the z dimension and xangle is the angle which affects the X
        """
        z = np.cos(zangle) ** -1
        x = np.cos(xangle) ** -1
        circle = self.sphere(n_points)
        for idx, p in enumerate(circle):
            circle[idx] = Point(p.x * x, p.y, p.z * z)
        return circle

