from random import *
from pygame import *
from math import *
from constants import *
from tools import *


def check(co):
    if 0 <= co[0][0] <= width - 1 and 0 <= co[0][1] <= height - 1 and co[1]:
        return True
    return False


def draw_point(direct, po, coor, col):
    midvec = Vector.points(direct.position, po)
    distance = sqrt(midvec * midvec)
    draw.circle(screen, col, coor[0], 30 / distance, 100)


init()
screen = display.set_mode((width, height))
display.set_caption("3D")


def run(points, point_colors, connections, connection_colors, direct):
    running = True

    while running:
        clock = time.Clock()
        clock.tick(FPS)
        # key inputs
        for q in event.get():
            if q.type == QUIT:
                running = False
        keys = key.get_pressed()
        if keys[119]:
            # w
            direct.position.x += v
        if keys[115]:
            # s
            direct.position.x -= v
        if keys[97]:
            # a
            direct.position.y += v
        if keys[100]:
            # d
            direct.position.y -= v
        if keys[103]:
            # g - debug
            pri(direct.position)
            for i in range(len(points)):
                print(c(point_to_screen(direct, points[i])))

        # Points to coordinates
        coordinates = [c(point_to_screen(direct, points[i])) for i in range(len(points))]

        # filling screen
        screen.fill(WHITE)
        for i in range(len(points)):
            if check(coordinates[i]):
                draw_point(direct, points[i], coordinates[i], point_colors[i])
            else:
                continue
        for i in range(len(connections)):
            if coordinates[connections[i][0]][1] and coordinates[connections[i][1]][1]:
                draw.line(screen, connection_colors[i], coordinates[connections[i][0]][0],
                          coordinates[connections[i][1]][0])
            elif coordinates[connections[i][0]][1]:
                draw.line(screen, connection_colors[i], coordinates[connections[i][0]][0],
                          c(back_point(points[connections[i][1]], points[connections[i][0]], direct))[0])
            elif coordinates[connections[i][1]][1]:
                draw.line(screen, connection_colors[i],
                          c(back_point(points[connections[i][0]], points[connections[i][1]], direct))[0],
                          coordinates[connections[i][1]][0])
        display.update()
