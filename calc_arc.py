"""Calculates l1, l2, and l3 for n points in a spherical detector with distance d"""
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from mpl_toolkits.mplot3d import Axes3D
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
                plane = Plane(start, middle, end)

                start_projection = plane.project(start)
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
                times.append(((l1, l2 * ref_index, l3), start, middle, end))
    return times


sphere_radius = 6
index_refraction = .2

emitters = [Point(-10, 0, 0)]
detectors = [Point(0, 4, 0)]
receivers = [Point(10, uniform(-5, 5), uniform(-5, 5)) for i in range(20)]

times = calc_times(emitters, detectors, receivers, sphere_radius, index_refraction)
max_time = max([sum(t[0]) for t in times])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw arcs
for time, start, middle, end in times:
    time = sum(time)
    color = (time/ max_time, (max_time - time) / max_time, 0, 1)
    ax.plot([start[0], middle[0]], [start[1], middle[1]], [start[2], middle[2]], c=color)
    ax.plot([end[0], middle[0]], [end[1], middle[1]], [end[2], middle[2]], c=color)


# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v) * sphere_radius
y = np.sin(u)*np.sin(v) * sphere_radius
z = np.cos(v) * sphere_radius
ax.plot_wireframe(x, y, z, color=(0, 0, .5, .1))

# Draw emitters and stuff
ex, ey, ez = zip(*emitters)
dx, dy, dz = zip(*detectors)
rx, ry, rz = zip(*receivers)
ax.scatter(ex, ey, ez, c="red")
ax.scatter(dx, dy, dz, c="blue")
ax.scatter(rx, ry, rz, c="green")

# Set up and display graph
ax.set_ylim((-10, 10))
ax.set_xlim((-10, 10))
ax.set_zlim((-10, 10))

plt.show()
fig.savefig('plotcircles.png')
