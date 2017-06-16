import numpy as np
"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
def slope(*points):
    return(points[0][1] - points[1][1]) / (points[0][0] - points[1][0])


def midpoint(*points):
    return (points[0][0] + points[1][0]) * .5, (points[0][1] + points[1][1]) * .5


def radius(*points):
    """ Complex solution for the radius of a circle from 3 points """
    p1, p2, p3 = [complex(*p) for p in points]
    diff = p1 - p3
    diff /= p2 - p1
    center = (p1 - p2) * (diff - abs(diff) **2) / 2j /diff.imag - p1
    return abs(center + p1)

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
    for emitter in range(num_points):
        for detector in range(num_points):
            for reciever in range(num_points):

                e_coord = (-width/2, separation * (emitter + 1))
                d_coord = (0, separation * (detector + 1))
                r_coord = (width/2, separation * (reciever + 1))

                large_radius = radius(e_coord, d_coord, r_coord)

                chord = (sphere_radius ** 2 - (large_radius - sphere_radius) ** 2) ** .5
                arc_radians = 4 * np.arcsin(x ** 2 / (2 * large_radius))
                l2 = large_radius * arc_radians
