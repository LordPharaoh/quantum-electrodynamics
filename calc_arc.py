"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import uniform
from geometry import Plane, Vector, Circle, Point


def arc3d(start, p2, end, num_points):
    """ returns num_points points on the 3d arc containing p1, p2, and p3, starting at p1 and ending at p3"""
    plane = Plane(start, p2, end)
    pr1 = plane.project(start)
    pr2 = plane.project(p2)
    pr3 = plane.project(end)
    circle = Circle(pr1, pr2, pr3)

    radian_len = circle.chord_angle(pr1.distance(pr3))
    increment = radian_len / num_points
    diff = pr1 - circle.center
    offset = np.arctan(diff.y / diff.x)
    # the range of arcsin is from -90 to 90 so (or radians but that's harder to type)
    if diff.x < 0:
        offset += np.pi / 2

    points3d = []
    for p in range(num_points):
        radian = increment * p - offset
        point = circle.center + Vector(np.sin(radian) * circle.radius, np.cos(radian) * circle.radius)
        points3d.append(plane.unproject(point))
    points3d.append(end)
    return points3d


def points_to_plt(l_points):
    """ Takes a list of points and returns a list containing a list of each dimension """
    x, y, z = zip(*l_points)
    return x, y, z


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

                l1 = large.arc_length(start_projection, e_pt)
                l2 = large.arc_length(e_pt, r_pt)
                l3 = large.arc_length(r_pt, end_projection)
                times.append(((l1, l2 * ref_index, l3), start, middle, end, plane.unproject(e_pt), plane.unproject(r_pt)))
    return times


sphere_radius = 6
index_refraction = .2

emitters = [Point(-10, 0, 0)]
detectors = [Point(0, uniform(-5, 5), uniform(-3, 3)) for i in range(10)]
#receivers = [Point(10, uniform(-5, 5), uniform(-3, 3)) for i in range(10)]
receivers = [Point(10, 0, 0)]

times = calc_times(emitters, detectors, receivers, sphere_radius, index_refraction)
max_time = max([sum(t[0]) for t in times])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw arcs
for lengths, start, middle, end, e_pt, r_pt in times:
    time = sum(lengths)
    color = (time/ max_time, (max_time - time) / max_time, 0, 1)
    ax.plot(*points_to_plt(arc3d(start, middle, end, 50)), c=color)
    ax.scatter(*points_to_plt([e_pt, r_pt]), c=color)
    ax.scatter(*points_to_plt([start, middle, end]), c="blue")

# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v) * sphere_radius
y = np.sin(u)*np.sin(v) * sphere_radius
z = np.cos(v) * sphere_radius
ax.plot_wireframe(x, y, z, color=(0, 0, .5, .1))

# Set up and display graph
ax.set_ylim((-10, 10))
ax.set_xlim((-10, 10))
ax.set_zlim((-10, 10))

plt.show()
fig.savefig('plotcircles.png')
