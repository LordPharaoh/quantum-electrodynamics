"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
import numpy as np

def slope(*points):
    return(points[0][1] - points[1][1]) / (points[0][0] - points[1][0])


def midpoint(*points):
    return (points[0][0] + points[1][0]) * .5, (points[0][1] + points[1][1]) * .5


def radius(*points):
    """ Calculate the radius of a circle based on 3 points """
    # perpendicular slope of both chords

    pt1, pt2, pt3 = points

    perp_slope_0 = 0
    perp_slope_1 = 0

    for i in range(3):
        try:
            perp_slope_0 = -(slope(pt1, pt2) ** -1)
            perp_slope_1 = -(slope(pt2, pt3) ** -1)
            break
        except ZeroDivisionError:
            # TODO this doesn't cover all orderings but it mostly works
            pt1, pt2, pt3 = pt3, pt1, pt2

    if perp_slope_0 == 0 and perp_slope_1 == 0:
        raise ValueError("Given points are co-linear, cannot make a circle")

    diff_slope = perp_slope_1 - perp_slope_0

    if diff_slope == 0:
        raise ValueError("Given points are co-linear, cannot make a circle")

    offset_0 = perp_slope_0 * -midpoint(pt1, pt2)[0] + midpoint(pt1, pt2)[1]
    offset_1 = perp_slope_1 * -midpoint(pt2, pt3)[0] + midpoint(pt2, pt3)[1]
    print(pt1, pt2, pt3)

    x = (offset_1 - offset_0) / diff_slope
    y = perp_slope_0 * (x - midpoint(pt1, pt2)[0]) + midpoint(pt1, pt2)[1]

    radius = ((pt1[0] - x) ** 2 + (pt1[1] - y) ** 2) ** .5

    return radius


def overlapping_chord(r1, r2):
    return (r1**2 - (r2 - r1) ** 2) ** .5


def chord_angle(chord, radius):
    return 2 * np.arcsin(x/(2*radius))

def calc_arc(num_points, sphere_radius, height, width):
    # if an odd number is entered for num_points, it will just do num_points - 1 since the center point can't have an
    # arc through it
    if num_points % 2 != 0:
        num_points -= 1
    if num_points <= 0:
        raise ValueError("Number of points was equal to or less than 1.")
    # dist between each point
    # padding from top and bottom
    # delete '+ 2' to remove padding
    separation = height / (num_points + 2)
    for i in range(num_points):
        current_height = (i + 1) * separation
        # arcs can't be flat
        # calculates the radius of the circle created by the 3 points on the separator
        large_radius = abs((width ** 2)/(8 * current_height)) + (current_height * .5)

print(radius((3, 4), (-3, 4), (3, -4)))
