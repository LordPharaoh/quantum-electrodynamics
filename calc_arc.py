"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
from random import uniform
from geometry import Plane, Vector, Circle, Point


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

                #plane = Plane(start, middle, end)

                if Point.collinear(start, middle, end):
                    continue

                # sometimes it doesn't get that points are collinear because of floating point misses
                # and then it winds up with complex numbers and breaks
                # and rounding doesn't seem to help
                # So i'ma just skip those
                large = Circle(start, middle, end)
                small = Circle(sphere_radius, (0, 0))

                inter_pts = large.intersection(small)
                e_pt, r_pt = (min(inter_pts, key=lambda x: x.distance(start)),
                              max(inter_pts, key=lambda x: x.distance(start)))

                l1 = large.arc_length(start, e_pt)
                l2 = large.arc_length(e_pt, r_pt)
                l3 = large.arc_length(r_pt, end)
                times.append(((l1, l2 * ref_index, l3), large, inter_pts))
    return times

# so maybe I've gone sliiiightly overboard with those list comprehensions
times = calc_times([Point(-10, 0)], [Point(0, uniform(-5, 5)) for i in range(50)], [Point(10, uniform(-5, 5))
                                                                                    for i in range(50)], 6, .2)
fig, ax = plt.subplots()
ax.set_xlim((-10, 10))
ax.set_ylim((-10, 10))
max_time = max([sum(t[0]) for t in times])
for time, circle, inter_pts in times:
    time = sum(time)
    angles = (np.arctan(p.slope(circle.center)) for p in inter_pts)
    color = (time/ max_time, (max_time - time) / max_time, 0, .1)
    ax.add_patch(ptch.Arc(circle.center, circle.radius * 2, circle.radius * 2, 0, *angles, edgecolor=color))

ax.add_artist(plt.Circle((0, 0), 6, color='blue', fill=False))

fig.savefig('plotcircles.png')
