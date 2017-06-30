"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
from __future__ import division
import numpy as np
from geometry import Plane, Circle, Point
from pipeline import msg
from random import uniform


def sph2cart(azimuth, elevation, r):
    x = r * np.cos(elevation) * np.cos(azimuth)
    y = r * np.cos(elevation) * np.sin(azimuth)
    z = r * np.sin(elevation)
    return Point(x, y, z)


def random_angle():
    # Only positive angles cuz reasons
    return uniform(0, np.pi)


def calc_norm(emitters, middles, detectors, sphere_radius, ref_index, display=False):
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
    norms = []
    intersections = []
    q_values = []
    # FIXME figure out what this is
    delta = 7.7018
    # wavelength for a given energy of light
    wavelength = .123989

    for start in emitters:
        for end in detectors:
            detector_sum = 0
            for middle in middles:

                plane = Plane(start, middle, end)

                assert abs(middle) < sphere_radius, \
                    "Middle point {} outside sphere of radius {}".format(middle, sphere_radius)

                start_projection = plane.project(start)
                # FIXME for some reason just the middle point is flipped on the y axis.
                # Who knows why, but somebody should find out
                # middle_projection = plane.project(Point(middle.x, -middle.y, middle.z))
                middle_projection = plane.project(middle)
                end_projection = plane.project(end)

                if Point.collinear(start_projection, middle_projection, end_projection):
                    continue

                # somenorms it doesn't get that points are collinear because of floating point misses
                # and then it winds up with complex numbers and breaks
                # and rounding doesn't seem to help
                # So i'ma just skip those
                large = Circle(start_projection, middle_projection, end_projection)
                # Find out the radius of the sphere at this location
                dist = plane.distance(Point(0, 0, 0))
                angle = np.arccos(plane.distance(Point(0, 0, 0)) / sphere_radius)
                small = Circle(sphere_radius * np.sin(angle), plane.project(Point(0, 0, 0)))

                # Getting these really weird errors, possibly floating point issues
                try:
                    inter_pts = large.intersection(small)
                except ValueError:
                    print("Circles did not intersect?")
                    continue

                e_pt, r_pt = (min(inter_pts, key=lambda x: x.distance(start_projection)),
                              max(inter_pts, key=lambda x: x.distance(start_projection)))

                intersections.append(plane.unproject(e_pt))
                intersections.append(plane.unproject(r_pt))

                len1 = large.arc_length(start_projection, e_pt) * 1e9
                len2 = large.arc_length(e_pt, r_pt) * 1e9
                len3 = large.arc_length(r_pt, end_projection) * 1e9

                phase1 = np.angle(np.exp(2 * np.pi * delta * 1j * len1)) + delta * np.pi
                phase2 = np.angle(np.exp(2 * np.pi * delta * ref_index * 1j * len2)) + phase1 + delta * np.pi
                phase3 = np.angle(np.exp(2 * np.pi * delta * 1j * len3)) + phase2

                wave = np.exp(phase3 * 1j)

                detector_sum += wave.imag

                # angle to detector from center of sphere
            if not display:
                angle_to_detector = np.tan(float(end.z) / end.y) / 2
                q = 4 * np.pi * np.sin(angle_to_detector) / wavelength
                q_values.append(q)

            norms.append(np.log(detector_sum ** 2))

    if not display:
        return norms, q_values
    else:
        return norms, intersections

