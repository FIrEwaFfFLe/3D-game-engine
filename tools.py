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
    elif t(inp) == "Plane":
        print(t(inp) + "(" + str(inp.a) + ", " + str(inp.b) + ", " + str(inp.c) + ", " + str(inp.d) + ")")


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
    cons = constants.width / (sqrt(3 * distance) * 2)
    # cons [pix / unit]
    che = direc.front * d
    return b(plane_coordinates(direc.left, direc.up, Vector.poi(Vector.points(direc.position, a)) * cons)) + \
           Coordinate(constants.width // 2, constants.height // 2), che != abs(che)


def plane_line(pl, p1, p2):
    # p1 -> p2 vector
    t = (pl.a * p1.x + pl.b * p1.y + pl.c * p1.z + pl.d) / \
        (pl.a * (p1.x - p2.x) + pl.b * (p1.y - p2.y) + pl.c * (p1.z - p2.z))
    t = p(t)
    if 0 <= t <= 1:
        return p1 + Vector.points(p1, p2) * t
    else:
        return False


def edges(po, direct):
    # p1 - back point, p2 - orientating
    x = straight_distance(direct, po)
    vec1 = Vector.points(direct.position, x)
    dis = vec1 * vec1
    if dis == 0:
        dis = 0.01
    cons = sqrt(3 * dis)
    a, b = cons, 9 * cons / 16
    ans = Vector((direct.left.x == 0 and direct.up.x == 0) * (x.x - direct.position.x),
                 (direct.left.y == 0 and direct.up.y == 0) * (x.y - direct.position.y),
                 (direct.left.z == 0 and direct.up.z == 0) * (x.z - direct.position.z)) + direct.position
    return ans + direct.left * a + direct.up * b, \
           ans - direct.left * a + direct.up * b, \
           ans - direct.left * a - direct.up * b, \
           ans + direct.left * a - direct.up * b


def back_point(p1, p2, direct):
    # p1 - back one, p2 - front
    edg = edges(p2, direct)
    closest_point = Point(10000, 10000, 10000)
    closness = 0
    vir = True
    for i in range(4):
        if i != 3:
            k = plane_line(Plane.get(direct.position, edg[i], edg[i + 1]), p2, p1)
            if t(k) == "bool":
                continue
            x = Vector.points(p1, k)
            dis = x * x
            if dis > closness:
                closest_point = k
                closness = dis
                vir = False
        else:
            k = plane_line(Plane.get(direct.position, edg[3], edg[0]), p2, p1)
            if t(k) == "bool":
                continue
            x = Vector.points(p1, k)
            dis = x * x
            if dis > closness:
                closest_point = k
                closness = dis
                vir = False
    if not vir:
        return point_to_screen(direct, closest_point)
    else:
        return False


def solve(oy, ox, pos, a):
    pl = Plane.get(pos, pos + oy, pos + ox)
    si = sin(a)
    co = cos(a)
    znam = (pl.a * (oy.y * ox.z - ox.y * oy.z) - pl.b * (oy.x * ox.z - ox.x * oy.z) + pl.c * (oy.x * ox.y - ox.x * oy.y))
    x1 = (pl.b * (oy.z * si - ox.z * co) - pl.c * (oy.y * si - ox.y * co)) / znam
    y1 = (-pl.a * (oy.z * si - ox.z * co) + pl.c * (oy.x * si - ox.x * co)) / znam
    z1 = (pl.a * (oy.y * si - ox.y * co) - pl.b * (oy.x * si - ox.x * co)) / znam
    return Vector(x1, y1, z1)


def rotate_vector_count_clock(vec, si, co):
    return Vector(vec.x * co - vec.y * si, vec.x * si + vec.y * co, vec.z)


def horiz_rot(direct, a):
    si, co = sin(a), cos(a)
    direct.front = rotate_vector_count_clock(direct.front, si, co)
    direct.left = rotate_vector_count_clock(direct.left, si, co)
    direct.up = rotate_vector_count_clock(direct.up, si, co)
    return direct


def verti_rot(direct, a):
    vecy = direct.front
    vecx = direct.up
    checker = solve(vecy, vecx, direct.position, a + constants.quater)
    if 0 <= checker.z:
        direct.front = solve(vecy, vecx, direct.position, a)
        direct.up = checker
    return direct


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


class Plane:
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = p(a), p(b), p(c), p(d)

    @classmethod
    def get(cls, p1, p2, p3):
        a = (p1.y - p2.y) * (p2.z - p3.z) - (p3.y - p2.y) * (p2.z - p1.z)
        b = (p2.z - p3.z) * (p2.x - p1.x) + (p2.z - p1.z) * (p3.x - p2.x)
        c = (p1.y - p2.y) * (p3.x - p2.x) + (p3.y - p2.y) * (p2.x - p1.x)
        d = -(a * p1.x + b * p1.y + c * p1.z)
        return Plane(a, b, c, d)


# pov = Direct(Point(0, 0, 0.3551136363636364), Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))
# verti_rot(pov, pi / 4)
# horiz_rot(pov, constants.ro_v)
# pri(pov.front)
# pri(pov.left)
# pri(pov.up)
# ax, bx = Point.list(list(map(float, input().split(",")))), Point.list(list(map(float, input().split(","))))
# pri(back_point(bx, ax, pov)[0])
# pri(rotate_vector_count_clock(Vector(1, 0, 0), 0.5, sqrt(0.75)))
# edges(insp, pov)
# pri(point_to_screen(pov, insp)[0])

# pri(plane_line(Plane.get(Point.list(list(map(float, input().split(",")))),
#                         Point.list(list(map(float, input().split(",")))),
#                         Point.list(list(map(float, input().split(","))))),
#               Point.list(list(map(float, input().split(",")))),
#               Point.list(list(map(float, input().split(","))))))
