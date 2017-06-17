"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
from random import uniform
from math import isnan

#TODO vector class

def slope(*points):
    return(points[0][1] - points[1][1]) / (points[0][0] - points[1][0])


def midpoint(*points):
    return (points[0][0] + points[1][0]) * .5, (points[0][1] + points[1][1]) * .5


def dist(p1, p2):
    total = 0
    for v1, v2 in zip(p1, p2):
        total += (v1 - v2) ** 2
    return total ** .5


def vec_add(p1, p2):
    newvec = []
    for v1, v2 in zip(p1, p2):
        newvec.append(v1 + v2)
    return tuple(newvec)


def scalar_multiply(pt, scalar):
    return tuple([pt * i for i in scalar])

def collinear(*args):
    if args[0][0] == args[1][0]:
        for x, y in args:
            if x != args[0][0]:
                return False
    m = (args[0][1] - args[1][1]) / (args[0][0] - args[1][0])
    b = args[0][1] - (m * args[0][0])
    for x, y in args:
        if round(y, 5) != round(m*x + b, 5):
            return False
    return True


def cross_product(vec1, vec2):
    return [vec1[1] * vec2[2] - vec1[2] * vec2[1],
            -1 * (vec1[0] * vec2[2] - vec1[2] * vec2[0]),
            vec1[0] * vec2[1] - vec1[1] * vec2[0]]


class Circle(object):
    def __str__(self):
        return "radius:{} center:{}".format(self.radius, self.center)

    def __init__(self, *args):
        if len(args) == 3 and hasattr(args[1], '__iter__'):
            """ Complex solution for the radius of a circle from 3 points returns radius, centerx, centery """
            if collinear(*args):
                raise ValueError("Points used to init circle are collinear")
                return
            p1, p2, p3 = [complex(*p) for p in args]
            for i in range(3):
                try:
                    p1, p2, p3 = p3, p1, p2
                    diff = p3 - p1
                    diff /= p2 - p1
                    center = (p1 - p2) * (diff - abs(diff) **2) / 2j / diff.imag - p1
                    self.center = center.real, center.imag
                except ZeroDivisionError:
                    pass
            self.radius = abs(complex(*self.center) + p1)
            self.x = self.center[0]
            self.y = self.center[1]
        elif len(args) == 3:
            self.radius = args[0]
            self.x = args[1]
            self.y = args[2]
            self.center = (self.x, self.y)
        else:
            self.radius = args[0]
            self.center = args[1]
            self.x = self.center[0]
            self.y = self.center[1]

    def chord_angle(self, chord):
        return 2 * np.arcsin(chord/(2*self.radius))

    def intersection(self, other):
        """ 
        returns the points of overlap between 2 circles at a given distance
        """
        d = dist(other.center, self.center)
        if self.center == other.center:
            raise ValueError("Circles have the same center")
            return
        if d > self.radius + other.radius:
            raise ValueError("Circles do not touch")
            return
        mid_dst = (self.radius **2 - other.radius **2 + d **2) / (2 * d)
        relative_pt = [p * mid_dst / d for p in vec_add(other.center, [-1 * i for i in self.center])]
        mid_pt = vec_add(self.center, relative_pt)
        chord_len = 2 * (abs(self.radius ** 2 - mid_dst ** 2)) ** .5
        slope = chord_len / (2 * d)
        inter_pt = mid_pt[0] + slope * (other.y - self.y), mid_pt[1] - slope * (other.x - self.x)
        inter_pt2 = mid_pt[0] - slope * (other.y - self.y), mid_pt[1] + slope * (other.x - self.x)
        return inter_pt, inter_pt2

    def arc_length(self, p1, p2):
        central_angle = self.chord_angle(dist(p1, p2))
        return central_angle * self.radius

    def plt_circle(self, color='blue'):
        return plt.Circle(self.center, self.radius, color=color)


def Plane(object):

    def __init__(self, *args):
        if len(args) == 3 and all(hasattr(p, '__iter__') and len(p) == 3 for p in args):
            vec1 = vec_add(args[1], scalar_multiply(args[0], -1))
            vec2 = vec_add(args[2], scalar_multiply(args[0], -1))
            c_p = cross_product(vec1, vec2)

            self.a, self.b, self.c = c_p
            self.d = c_p[0] * args[0][1] + c_p[1] * args[0][1] + c_p[2] * args[0][2]


def calc_times(emitters, middles, detectors, sphere_radius, ref_index):
    """
    :param emitters: list of points of all x-ray emitters
    :param middles: list of points of all arc spots inside the sphere
    :param detectors: list of points of all detectors
    :param sphere_radius: radius of sphere of material
    :param ref_index: index of refraction of material with x-rays (*not* the 1- thing, TODO)
    :return: [(time_to_material, time_through_material, time_to_detector), ... ]
    """
    # dist between each point
    # padding from top and bottom
    # delete '+ 2' to remove padding
    times = []
    for start in emitters:
        for middle in middles:
            for end in detectors:

                plane = Plane(start, middle, end)

                if collinear(start, middle, end):
                    continue

                # sometimes it doesn't get that points are collinear because of floating point misses
                # and then it winds up with complex numbers and breaks
                # and rounding doesn't seem to help
                # So i'ma just skip those
                large = Circle(start, middle, end)
                small = Circle(sphere_radius, (0, 0))

                inter_pts = large.intersection(small)
                e_pt, r_pt = min(inter_pts, key=lambda x: dist(x, start)),  max(inter_pts, key=lambda x: dist(x, start))

                l1 = large.arc_length(start, e_pt)
                l2 = large.arc_length(e_pt, r_pt)
                l3 = large.arc_length(r_pt, end)
                times.append(((l1, l2 * ref_index, l3), large, inter_pts))
    return times

# so maybe I've gone sliiiightly overboard with those list comprehensions
# times = [( i[1].center, i[1].radius * 2, i[1].radius * 2, 0, np.arctan(slope(i[2][0], i[0].center)),
        #np.arctan(slope(i[1][0], i[0].center)), ((20-sum(i[0]/20)) for i in

times = calc_times([(-10, 0)], [(0, uniform(-5, 5)) for i in range(50)], [(10, uniform(-5, 5)) for i in range(50)], 6, .2)
fig, ax = plt.subplots()
ax.set_xlim((-10, 10))
ax.set_ylim((-10, 10))
max_time = max([sum(t[0]) for t in times])
for time, circle, inter_pts in times:
    time = sum(time)
    angles = (np.arctan(slope(p, circle.center)) for p in inter_pts)
    color = (time/ max_time, (max_time - time) / max_time, 0, .1)
    ax.add_patch(ptch.Arc(circle.center, circle.radius * 2, circle.radius * 2, 0, *angles, edgecolor=color))

ax.add_artist(plt.Circle((0, 0), 6, color='blue', fill=False))

fig.savefig('plotcircles.png')
