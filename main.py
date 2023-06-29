from random import *
from pygame import *
from math import *
from constants import *
from tools import *
import game


def rc():
    return randint(0, 200), randint(0, 200), randint(0, 200)


# points = [Point(6, i, j) for i in range(-10, 11) for j in range(-10, 11)]
points = [Point(2, 2, 1), Point(2, -2, 1), Point(2, 2, -1), Point(2, -2, -1),
          Point(5, 2, 1), Point(5, -2, 1), Point(5, 2, -1), Point(5, -2, -1)]
po_cols = [BLACK] * 500
connections = [(0, 1), (0, 2), (1, 3), (2, 3),
               (0, 4), (1, 5), (2, 6), (3, 7),
               (4, 5), (4, 6), (5, 7), (6, 7), (0, 6)]
connect_cols = [BLACK] * 500
direct = Direct(Point(0, 0, 0),
                Vector(1, 0, 0),
                Vector(0, 1, 0),
                Vector(0, 0, 1))


if __name__ == "__main__":
    game.run(points, po_cols, connections, connect_cols, direct)
