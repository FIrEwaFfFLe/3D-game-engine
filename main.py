from random import *
from pygame import *
from math import *
from constants import *
from tools import *
import game


def rc():
    return randint(0, 200), randint(0, 200), randint(0, 200)


# points = [Point(6, i, j) for i in range(-10, 11) for j in range(-10, 11)]
points = [Point(2, 2, 1), Point(2, -2, 1), Point(2, -2, -1), Point(2, 2, -1),
          Point(5, 2, 1), Point(5, -2, 1), Point(5, -2, -1), Point(5, 2, -1)]
po_cols = [rc() for i in range(100)]
connections = [(0, 1), (1, 2), (2, 3), (0, 3),
               (4, 5), (5, 6), (6, 7), (4, 7),
               (0, 4), (1, 5), (2, 6), (3, 7),
               (0, 5), (1, 4), (0, 7), (3, 4),
               (5, 7), (4, 6), (1, 6), (2, 5),
               (3, 6), (2, 7)]
connect_cols = [rc() for i in range(100)]
direct = Direct(Point(0, 0, 0),
                Vector(1, 0, 0),
                Vector(0, 1, 0),
                Vector(0, 0, 1))


if __name__ == "__main__":
    game.run(points, po_cols, connections, connect_cols, direct)
