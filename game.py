from random import *
from pygame import *
from math import *
from constants import *
from tools import *


def draw_point(coor, col):
    draw.circle(screen, col, coor[1], 30 / coor[0], 100)


def draw_text(text, f, col, coor):
    img = f.render(text, True, col)
    screen.blit(img, coor)


init()
screen = display.set_mode((width, height))
display.set_caption("3D")
text_font = font.SysFont("Times New Roman", text_size)


def run(points, point_colors, connections, connection_colors, direct):
    running = True
    show_cor = False
    last_show_cor = -200
    last_debug = -200
    clip = 1

    while running:
        clock = time.Clock()
        clock.tick(FPS)
        # key inputs
        for q in event.get():
            if q.type == QUIT:
                running = False
        keys = key.get_pressed()
        current_speed = v
        if keys[1073742048]:
            current_speed *= multiply
        if keys[119]:
            # w
            direct.position += Vector(direct.left.y, -direct.left.x, direct.left.z) * current_speed
        if keys[115]:
            # s
            direct.position -= Vector(direct.left.y, -direct.left.x, direct.left.z) * current_speed
        if keys[97]:
            # a
            direct.position += direct.left * current_speed
        if keys[100]:
            # d
            direct.position -= direct.left * current_speed
        if keys[32]:
            # space
            direct.position.z += current_speed
        if keys[1073742049]:
            # shift
            direct.position.z -= current_speed
        if keys[1073741904]:
            # left arrow
            horiz_rot(direct, ro_v)
        if keys[1073741903]:
            # right arrow
            horiz_rot(direct, -ro_v)
        if keys[1073741906]:
            # up arrow
            verti_rot(direct, ro_v)
        if keys[1073741905]:
            # down arrow
            verti_rot(direct, -ro_v)
        if keys[103]:
            # g - debug
            if clip - last_debug > reaction_time:
                pri(direct.position)
                pri(direct.front)
                last_debug = clip
        if keys[121]:
            # y - show coordinates
            if clip - last_show_cor > reaction_time:
                show_cor = not show_cor
                last_show_cor = clip
        # Points to coordinates
        # (distance, coordinate, in/out of view scope)
        coordinates = [c(point_to_screen(direct, points[i])) for i in range(len(points))]
        # filling screen
        screen.fill(WHITE)
        # connections
        for i in range(len(connections)):
            if coordinates[connections[i][0]][2] and coordinates[connections[i][1]][2]:
                draw.line(screen, connection_colors[i], coordinates[connections[i][0]][1],
                          coordinates[connections[i][1]][1])
            elif coordinates[connections[i][0]][2]:
                fun = back_point(points[connections[i][1]], points[connections[i][0]], direct)
                if t(fun) == "bool":
                    continue
                draw.line(screen, connection_colors[i], coordinates[connections[i][0]][1], c(fun)[1])
            elif coordinates[connections[i][1]][2]:
                fun = back_point(points[connections[i][0]], points[connections[i][1]], direct)
                if t(fun) == "bool":
                    continue
                draw.line(screen, connection_colors[i], c(fun)[1], coordinates[connections[i][1]][1])
        # points
        for i in range(len(points)):
            if coordinates[i][2]:
                draw_point(coordinates[i], point_colors[i])
        if show_cor:
            draw_text("x: " + str(round(direct.position.x * 100) / 100) +
                      ", y: " + str(round(direct.position.y * 100) / 100) +
                      ", z: " + str(round(direct.position.z * 100) / 100), text_font, BLACK, (0, 0))
            draw_text(str(round(direct.front.x * 100) / 100) + ", " +
                      str(round(direct.front.y * 100) / 100) + ", " +
                      str(round(direct.front.z * 100) / 100), text_font, BLACK, (0, text_size))
        clip += 1
        clip %= M
        display.update()
