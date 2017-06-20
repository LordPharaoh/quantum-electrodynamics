import vectors as v
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle


class Vector(object):
    """ 
    I didn't mean to create a whole new vector class, I was using the one from vectors as well as a bunch of random
    helper functions from the beginning, and then I noticed the vectors.vector class was really bad an made an 
    improvement or two, and the next thing you know it's its own class
    """
    def __init__(self, *args):
        self.iterable = args
        self.x = self.iterable[0]
        self.y = self.iterable[1]
        self.z = self.iterable[1]
        self.a, self.b, self.c = self.x, self.y, self.z

    def slope(self, point):
        return (self.y - point.y) / (self.x - point.x)

    def midpoint(self, point):
        return Vector((self.x + point.x) * .5, (self.y + point.y) * .5)

    def distance(self, p2):
        total = 0
        for v1, v2 in zip(self, p2):
            total += (v1 - v2) ** 2
        return total ** .5

    def collinear(*args):
        if args[0].x == args[1].x:
            for x, y in args:
                if x != args[0].x:
                    return False
        m = (args[0].y - args[1].y) / (args[0].x - args[1].x)
        b = args[0].y - (m * args[0].x)
        for x, y in args:
            if round(y, 5) != round(m*x + b, 5):
                return False
        return True

    def __getitem__(self, n):
        return self.iterable.__getitem__(n)

    def __iter__(self):
        return self.iterable.__iter__()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(*[s + o for s, o in zip(self, other)])
        else:
            return Vector(*[i + other for i in self])

    def __mul__(self, other):
        if isinstance(other, Vector):
            total = 0
            for s, o in zip(self, other):
                total += s * o
            return total
        else:
            return Vector(*[i * other for i in self])

    def __sub__(self, other):
        return self + (other * -1)

    def __truediv__(self, other):
        return self * (other ** -1)

    def __matmul__(self, other):
        # Too lazy to do cross products myself
        return Vector(*v.Vector.from_list(self.iterable).cross(v.Vector.from_list(other.iterable)).vector)

    def __abs__(self):
        return self.distance(Vector(*[0 for i in self.iterable]))

    def __str__(self):
        return str("<{}>".format(str(self.iterable)[1:-1]))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.iterable)

    def cross(self, other):
        return self.__matmul__(other)
# easier to think about
Point = Vector


class Circle(object):
    """ Represents a 2 dimensional circle """
    def __str__(self):
        return "radius:{} center:{}".format(self.radius, self.center)

    @staticmethod
    def _perpendicular_bisector(point1, point2):
        mid = Point.midpoint(point1, point2)
        slope = Point.slope(point1, point2)
        m = -(slope ** -1)
        b = m * -mid.x + mid.y
        return m, b

    @staticmethod
    def _intersection(mb1, mb2):
        x = (mb2[1] - mb1[1]) / (mb1[0] - mb2[0])
        y = x * mb1[0] + mb1[1]
        return Point(x, y)

    def __init__(self, *args):
        if len(args) == 3 and all([isinstance(p, Point) for p in args]):
            """ Complex solution for the radius of a circle from 3 points returns radius, centerx, centery """
            if Point.collinear(*args):
                raise ValueError("s.Points used to init circle are collinear")
            points = list(args)
            for i in range(6):
                try:
                    self.center = self._intersection(Circle._perpendicular_bisector(points[0], points[1]),
                                                     Circle._perpendicular_bisector(points[1], points[2]))
                    break
                except ZeroDivisionError:
                    shuffle(points)
            self.radius = self.center.distance(points[0])
            self.x = self.center.x
            self.y = self.center.y
        elif len(args) == 3:
            self.radius = args[0]
            self.x = args[1]
            self.y = args[2]
            self.center = Point(self.x, self.y)
        else:
            self.radius = args[0]
            self.center = Point(*args[1])
            self.x = self.center.x
            self.y = self.center.y

    def chord_angle(self, chord):
        return 2 * np.arcsin(chord/(2*self.radius))

    def intersection(self, other):
        """ 
        returns the points of overlap between 2 circles at a given distance
        """
        d = abs(self.center - other.center)
        if self.center == other.center:
            raise ValueError("Circles have the same center")
        if d > self.radius + other.radius:
            raise ValueError("Circles do not touch")
        mid_dst = (self.radius ** 2 - other.radius ** 2 + d ** 2) / (2 * d)
        relative_pt = (other.center - self.center) * (mid_dst / d)
        mid_pt = self.center + relative_pt
        chord_len = 2 * (abs(self.radius ** 2 - mid_dst ** 2)) ** .5
        slope = chord_len / (2 * d)
        inter_pt = Point(mid_pt.x + slope * (other.y - self.y), mid_pt.y - slope * (other.x - self.x))
        inter_pt2 = Point(mid_pt.x - slope * (other.y - self.y), mid_pt.y + slope * (other.x - self.x))
        return inter_pt, inter_pt2

    def arc_length(self, p1, p2):
        central_angle = self.chord_angle(p1.distance(p2))
        return central_angle * self.radius

    def plt_circle(self, color='blue'):
        return plt.Circle(self.center, self.radius, color=color)


class Plane(object):
    """ Plane in 3D helps transform 2D Ops (especially circle) back and forth from 3D """
    def __init__(self, *args, _axis=True):

        if len(args) == 3 and all(isinstance(p, Point) for p in args):
            vec1 = args[0] - args[1]
            vec2 = args[1] - args[2]

            self.cross_product = vec1 @ vec2
            self.d = -1 * (self.cross_product * args[0])
            # equation of plane: ax+by+cz+d=0

            # for mapping points to 2d space

        elif len(args) == 4:
                self.cross_product = Vector(*args[:3])
                self.d = args[4]

        elif len(args) == 2 and isinstance(args[0], Vector) and isinstance(args[1], Point):
            self.cross_product = args[0]
            self.d = -1 * (self.cross_product * args[1])

        else:
            raise TypeError("Arguments must be either 3 Points, a Vector followed "
                            "by a Point, or 4 coefficients a, b, c, d")

        self.center = self.closest(Point(0, 0, 0))
        self.a, self.b, self.c = self.cross_product
        if _axis:
            self.x_axis = Plane(self.closest(Point(1, 0, 0)) - self.center, self.center, _axis=False)
            self.y_axis = Plane(self.x_axis.cross_product @ self.cross_product, self.center, _axis=False)

    def closest(self, point):
        t = -(self.cross_product * point + self.d) / (abs(self.cross_product) ** 2)
        return (self.cross_product * t) + point

    def distance(self, point):
        if isinstance(point, Point):
            return ((self.cross_product * point) + self.d) / abs(self.cross_product)

    def project(self, point):
        point = self.closest(point)
        y = self.y_axis.distance(point)
        x = self.x_axis.distance(point)
        return Point(x, y)

    def unproject(self, point):
        # WHAT THE HECK I worked this all out and typed it in and it worked first time
        # This has literally never happened to me before and I was fully expecting to check 3 pages of work
        # and typos over and over
        x_offset = (point.x * abs(self.x_axis.cross_product) - self.x_axis.d) / self.x_axis.a
        y_divisor = self.y_axis.b * self.x_axis.a - self.y_axis.a * self.x_axis.b
        y_term_1 = point.y * self.x_axis.a * abs(self.y_axis.cross_product)
        y_term_2 = self.y_axis.d * self.x_axis.a
        y_term_3 = self.y_axis.a * self.x_axis.a * x_offset
        y_offset = (y_term_1 - y_term_2 - y_term_3) / y_divisor
        y_coefficient = (self.y_axis.a * self.x_axis.c - self.x_axis.a * self.y_axis.c) / y_divisor
        z_offset = -self.a * x_offset + ((self.a * self.x_axis.b * y_offset) / self.x_axis.a) - self.b * y_offset
        z_divisor = -((self.a * self.x_axis.b * y_coefficient) / self.x_axis.a) \
                    - ((self.a * self.x_axis.c)/self.x_axis.a) + self.b * y_coefficient + self.c
        z = z_offset / z_divisor
        y = y_offset + y_coefficient * z
        x = x_offset + ((-self.x_axis.b * y - self.x_axis.c * z)/self.x_axis.a)
        return Vector(x, y, z) + self.center

    def __str__(self):
        return "Plane: {}x + {}y + {}z + {} = 0".format(*self.cross_product, self.d)

