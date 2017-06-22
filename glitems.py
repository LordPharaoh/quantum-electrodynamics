from __future__ import division
import pyqtgraph.opengl as gl
from geometry import Plane, Circle, Vector
import numpy as np


class Sphere(gl.GLMeshItem):

    def __init__(self, center, radius, color=(0, 0, 1, .1)):
        self.mesh_data = gl.MeshData.sphere(rows=20, cols=20)
        super(Sphere, self).__init__(meshdata=self.mesh_data, smooth=True, color=color, shader='shaded')
        self.translate(*center)
        self.scale(radius, radius, radius)


class Arc(gl.GLLinePlotItem):

    def __init__(self, start, p2, end, color=(0, 1, 0, .3), num_points=50):
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
        else:
            offset -= np.pi / 2

        points3d = []
        for p in range(num_points):
            radian = increment * p - offset
            point = circle.center + Vector(np.sin(radian) * circle.radius, np.cos(radian) * circle.radius)
            points3d.append(plane.unproject(point))
        points3d.append(end)
        super(Arc, self).__init__(pos=np.array(points3d), color=color, width=2, antialias=True, mode='line_strip')


class Scatter(gl.GLScatterPlotItem):
    def __init__(self, points, color=(1, 0, 0, 1)):
        super(Scatter, self).__init__(pos=points, color=color, size=.5, pxMode=False)
