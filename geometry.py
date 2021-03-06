from __future__ import division
import numpy as np
from random import shuffle


class Vector(list):
    """ 
    I didn't mean to create a whole new vector class, I was using the one from vectors as well as a bunch of random
    helper functions from the beginning, and then I noticed the vectors.vector class was really bad an made an 
    improvement or two, and the next thing you know it's its own class
    """
    def __init__(self, *args):
        if len(args) == 1:
            # If a list is passed in it will be nested (args = [[otherlist]]
            super(Vector, self).__init__(args[0])
            self.order = len(args[0]) - 1
        else:
            self.order = len(args) - 1
            super(Vector, self).__init__(args)
        self.x = self[0]
        self.y = self[1]
        self.z = 0 if len(self) < 3 else self[2]
        self.a, self.b, self.c = self.x, self.y, self.z

    def slope(self, point):
        return (self.y - point.y) / (self.x - point.x)

    def midpoint(self, point):
        return Vector((self.x + point.x) * .5, (self.y + point.y) * .5, (self.z + point.z) * .5)

    def distance(self, p2):
        total = 0
        for v1, v2 in zip(self, p2):
            total += (v1 - v2) ** 2
        return total ** .5

    def collinear(*args):
        """ True if any number of given 2-dimensional points are collinear """
        slope = args[0].slope(args[1])
        for i in args[2:]:
            if args[0].slope(i) != slope:
                return False
        return True

    def complex(self):
        return self.x + self.y * 1j

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(*[s + o for s, o in zip(self, other)])
        else:
            return Vector(*[i + other for i in self])

    def __mul__(self, other):
        """ Returns dot product if multiplied by a vector or a scalar product vector if multipled by a scalar"""
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
        return Vector(np.cross(self, other))

    def cross(self, other):
        # This should be the new python3 "across" operator (@) but just in case we need python2
        # Too lazy to do cross products myself
        return Vector(np.cross(self, other))

    def __abs__(self):
        return self.distance(Vector(*[0 for i in self]))

    def __str__(self):
        ret = "<"
        for i in self:
            ret += str(i) + ", "
        return ret[:-2] + ">"

    def __repr__(self):
        return self.__str__()


# easier to think about
Point = Vector


class Circle(object):
    """ Represents a 2 dimensional circle """
    def __str__(self):
        return "radius:{} center:{}".format(self.radius, self.center)

    @staticmethod
    def _perpendicular_bisector(point1, point2):
        """ Slope and y-intercept of the perpendicular bisector of 2 Point, internal use """
        mid = Point.midpoint(point1, point2)
        slope = Point.slope(point1, point2)
        m = -(slope ** -1)
        b = m * -mid.x + mid.y
        return m, b

    @staticmethod
    def _intersection(mb1, mb2):
        """ Intersection of 2 lines with given slope and y-intercept, internal use """
        x = (mb2[1] - mb1[1]) / (mb1[0] - mb2[0])
        y = x * mb1[0] + mb1[1]
        return Point(x, y)

    def __init__(self, *args):
        """ Takes 3 points or radius, x, y or radius, xy """
        if len(args) == 3 and all([isinstance(p, Point) for p in args]):
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
        """ Returns the internal angle of a chord of given length """
        return 2 * np.arcsin(chord/(2*self.radius))

    def intersection(self, other):
        """ 
        returns the intersection points between 2 circles
        """
        d = self.center.distance(other.center)
        # no touchy or all touchy, nothing that we return will be useful
        if self.center == other.center:
            raise ValueError("No intersection point, centers are the same")
        # no touchy
        mid_dst = (self.radius ** 2 - other.radius ** 2 + d ** 2) / (2 * d)
        relative_pt = (other.center - self.center) * (mid_dst / d)
        mid_pt = self.center + relative_pt
        chord_len = 2 * (abs(self.radius ** 2 - mid_dst ** 2)) ** .5
        slope = chord_len / (2 * d)
        inter_pt = Point(mid_pt.x + slope * (other.y - self.y), mid_pt.y - slope * (other.x - self.x))
        inter_pt2 = Point(mid_pt.x - slope * (other.y - self.y), mid_pt.y + slope * (other.x - self.x))

        if d > self.radius + other.radius:
            raise ValueError("No intersection point, radii are too small")

        return inter_pt, inter_pt2

    def arc_length(self, p1, p2):
        """ Returns the length of an arc defined by 2 points on the circle """
        central_angle = self.chord_angle(p1.distance(p2))
        return central_angle * self.radius

    def filled_midpoint(self):
        """ Returns a list of points to create a pixelated filled-midpoint circle """
        range_ = int(self.radius / np.sqrt(2))
        points = []
        for i in range(self.radius, range_ - 1, -1):
            j = int(np.sqrt(self.radius ** 2 - i ** 2))
            for k in range(-j, j + 1):  
                points.append(Point(self.x - k, self.y + i))
                points.append(Point(self.x - k, self.y - i))
                points.append(Point(self.x + k, self.y - i))
                points.append(Point(self.x + k, self.y + i))
        range_ = int(self.radius * np.sin(np.pi / 4))
        for i in range(self.x - range_ + 1, self.x + range_):
            for j in range(self.y - range_ + 1, self.y + range_):
                points.append(Point(i, j))
        
        return points


class Plane(object):
    """ Plane in 3D helps transform 2D Ops (especially circle) back and forth from 3D """
    # kwargs isn't necessary but in pyth2 you can't have named kwargs before *args and I really want normal args before
    # essentially internal oens
    def __init__(self, *args, **kwargs):
        """
        :param args: 3 Points, 4 float coefficients, or a Vector and a Point
        :param kwargs: boolean _axis (internal use)
        """
        # Construct plane from 3 points
        if len(args) == 3 and all(isinstance(p, Point) for p in args):
            vec1 = args[0] - args[1]
            vec2 = args[1] - args[2]

            self.cross_product = vec1.cross(vec2)
            self.d = -1 * (self.cross_product * args[0])
            # equation of plane: ax+by+cz+d=0

        # Construct plane from 4 coefficients
        elif len(args) == 4:
            self.cross_product = Vector(*args[:3])
            self.d = args[3]

        # Construct plane from a cross-product Vector and a Point
        elif len(args) == 2 and isinstance(args[0], Vector) and isinstance(args[1], Point):
            self.cross_product = args[0]
            self.d = -1 * (self.cross_product * args[1])

        else:
            raise TypeError("Arguments must be either 3 Points, a Vector followed "
                            "by a Point, or 4 coefficients a, b, c, d")

        # Define an arbitrary center to project points onto. It's best to do the origin because if the sphere is at the
        # origin then finding its radius with an arbitrary plane slice is easy
        self.center = self.closest(Point(0, 0, 0))
        # useful shortcuts
        self.a, self.b, self.c = self.cross_product

        # Make 2 orthogonal planes to be the 'axes' if necessary, don't do this repetitively because recursion
        if kwargs.get("_axis", True):
            self.x_axis = Plane(self.closest(Point(1, 0, 0)) - self.center, self.center, _axis=False)
            self.y_axis = Plane(self.x_axis.cross_product.cross(self.cross_product), self.center, _axis=False)

    def closest(self, point):
        """ Finds the point on the plane closest to a point in 3D space """
        # Math
        t = -(self.cross_product * point + self.d) / (abs(self.cross_product) ** 2)
        return (self.cross_product * t) + point

    def distance(self, point):
        """ Finds the distance between a plane and a point """
        return ((self.cross_product * point) + self.d) / abs(self.cross_product)

    def project(self, point):
        """ Project a point in 3D space onto a 2D Cartesian plane anywhere in space """
        point = self.closest(point)
        y = self.y_axis.distance(point)
        x = self.x_axis.distance(point)
        return Point(x, y)

    def unproject(self, point):
        """ Take a point on the 2D Cartesian plane and find its 3D coordinates """
        # WHAT THE HECK I worked this all out and typed it in and it worked first time
        # This has literally never happened to me before and I was fully expecting to check 3 pages of work
        # and typos over and over
        # actually the first time I've done this much math and it's all been correct
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
        # I am done with this math roller coaster wheee

    def __str__(self):
        return "Plane: {}x + {}y + {}z + {} = 0".format(self.cross_product.x, self.cross_product.y,
                                                        self.cross_product.z, self.d)

