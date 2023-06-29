from math import *
import constants


def p(n):
    if abs(n // 1 - n) < 10e-9:
        return round(n)
    return n


def t(x):
    halfway = str(type(x))[8:-2]
    if halfway[0] == "_":
        return halfway[9:]
    while halfway.count(".") > 0:
        halfway = halfway[halfway.index(".") + 1:]
    return halfway


def b(x):
    if t(x) in ["Vector", "Point"]:
        return Vector(-x.x, -x.y, -x.z)
    elif t(x) == "Coordinate":
        return Coordinate(-x.x, -x.y)


def c(x):
    return (x[0].x, x[0].y), x[1]


def pri(inp):
    if t(inp) in ["Vector", "Point"]:
        print(t(inp) + "(" + str(inp.x) + ", " + str(inp.y) + ", " + str(inp.z) + ")")
    elif t(inp) == "Coordinate":
        print(t(inp) + "(" + str(inp.x) + ", " + str(inp.y) + ")")


def straight_distance(direc, c):
    a = direc.position
    vector1, vector2 = direc.front, Vector.points(a, c)
    k = p(vector1 * vector2 / (vector1 * vector1))
    return a + vector1 * k


def plane_coordinates(i, j, a):
    if i.z * j.y != j.z * i.y:
        return Coordinate((a.z * j.y - j.z * a.y) / (i.z * j.y - j.z * i.y),
                          (a.z * i.y - i.z * a.y) / (j.z * i.y - i.z * j.y))
    elif i.x * j.y != j.x * i.y:
        return Coordinate((a.x * j.y - j.x * a.y) / (i.x * j.y - j.x * i.y),
                          (a.x * i.y - i.x * a.y) / (j.x * i.y - i.x * j.y))
    elif i.z * j.x != j.z * i.x:
        return Coordinate((a.z * j.x - j.z * a.x) / (i.z * j.x - j.z * i.x),
                          (a.z * i.x - i.z * a.x) / (j.z * i.x - i.z * j.x))


def point_to_screen(direc, a):
    d = Vector.points(straight_distance(direc, a), direc.position)
    distance = d * d
    a += d
    if distance == 0:
        distance = 0.01
    cons = sqrt((constants.width ** 2) / (12 * distance))
    che = direc.front * d
    return b(plane_coordinates(direc.left, direc.up, Vector.poi(Vector.points(direc.position, a)) * cons)) + \
           Coordinate(constants.width // 2, constants.height // 2), che != abs(che)


class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = p(x), p(y), p(z)

    def __mul__(self, var):
        if t(var) == "Vector":
            return p(self.x * var.x + self.y * var.y + self.z * var.z)
        elif t(var) in ["int", "float"]:
            return Vector(var * self.x, var * self.y, var * self.z)

        print("__mul__ in Vector, no such multiplication companion")
        print(1 / 0)

    def __add__(self, var):
        if t(var) == "Vector":
            return Vector(self.x + var.x, self.y + var.y, self.z + var.z)
        elif t(var) == "Point":
            return Point(self.x + var.x, self.y + var.y, self.z + var.z)

        print("__add__ in Vector, no such addition companion")
        print(1 / 0)

    def __sub__(self, var):
        if t(var) == "Vector" or t(var) == "Point":
            return Vector(self.x - var.x, self.y - var.y, self.z - var.z)

        print("__sub__ in Vector, no such subtraction companion")
        print(1 / 0)

    @classmethod
    def points(cls, po1, po2):
        if t(po1) == "Point" and t(po2) == "Point":
            return Vector(po2.x - po1.x, po2.y - po1.y, po2.z - po1.z)
        else:
            print("Vector definition isn't in points")
            print(1 / 0)

    @classmethod
    def list(cls, li):
        return Vector(li[0], li[1], li[2])

    @classmethod
    def poi(cls, var):
        return Point(var.x, var.y, var.z)


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = p(x), p(y), p(z)

    def __mul__(self, var):
        if t(var) in ["int", "float"]:
            return Point(var * self.x, var * self.y, var * self.z)

        print("__mul__ in Point, no such multiplication companion")
        print(1 / 0)

    def __add__(self, var):
        if t(var) == "Vector":
            return Point(self.x + var.x, self.y + var.y, self.z + var.z)

        print("__add__ in Point, no such addition companion")
        print(1 / 0)

    def __sub__(self, var):
        if t(var) == "Vector":
            return self + b(var)

        print("__sub__ in Point, no such subtraction companion")
        print(1 / 0)

    @classmethod
    def list(cls, li):
        return Point(li[0], li[1], li[2])

    @classmethod
    def vec(cls, var):
        return Vector(var.x, var.y, var.z)


class Direct:
    def __init__(self, pos, vec_for, vec_lef, vec_up):
        self.position = pos
        self.front = vec_for
        self.up = vec_up
        self.left = vec_lef


class Coordinate:
    def __init__(self, x, y):
        self.x, self.y = p(x), p(y)

    def __mul__(self, var):
        if t(var) in ["int", "float"]:
            return Coordinate(self.x * var, self.y * var)

        print("__mul__ in Coordinate, no such multiplication companion")
        print(1 / 0)

    def __add__(self, var):
        if t(var) == "Coordinate":
            return Coordinate(self.x + var.x, self.y + var.y)

        print("__add__ in Coordinate, no such addition companion")
        print(1 / 0)

    def __sub__(self, var):
        # basically it's adding a 2d vector
        if t(var) == "Coordinate":
            return self + b(var)

        print("__sub__ in Coordinate, no such subtraction companion")
        print(1 / 0)

# pov = Direct(Point(3.2349999999999532, 1.4749999999999908, 0), Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))
# insp = Point.list(list(map(float, input().split())))
# pri(point_to_screen(pov, insp))
