"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
from __future__ import division
import numpy as np
from geometry import Plane, Circle, Point


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

                start_projection = plane.project(start)
                # FIXME for some reason just the middle point is flipped on the y axis.
                # Who knows why, but somebody should find out
                # middle_projection = plane.project(Point(middle.x, -middle.y, middle.z))
                middle_projection = plane.project(middle)
                end_projection = plane.project(end)

                if Point.collinear(start_projection, middle_projection, end_projection):
                    continue

                # sometimes it doesn't get that points are collinear because of floating point misses
                # and then it winds up with complex numbers and breaks
                # and rounding doesn't seem to help
                # So i'ma just skip those
                large = Circle(start_projection, middle_projection, end_projection)
                # Find out the radius of the sphere at this location
                angle = np.arccos(plane.distance(Point(0, 0, 0)) / sphere_radius)
                small = Circle(sphere_radius * np.sin(angle), plane.project(Point(0, 0, 0)))

                inter_pts = large.intersection(small)
                e_pt, r_pt = (min(inter_pts, key=lambda x: x.distance(start_projection)),
                              max(inter_pts, key=lambda x: x.distance(start_projection)))

                len1 = large.arc_length(start_projection, e_pt)
                len2 = large.arc_length(e_pt, r_pt)
                len3 = large.arc_length(r_pt, end_projection)
                times.append((len1, len2 * ref_index, len3))
    return times

