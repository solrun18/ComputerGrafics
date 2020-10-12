
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from random import *
from math import *

xxx_pos = 100
xxy_pos = 100
xyx_pos = 100
xyy_pos = 200
yyx_pos = 200
yyy_pos = 200
yxx_pos = 200
yxy_pos = 100

xxx_offset = 0.1
xxy_offset = 0.1
xyx_offset = 0.1
xyy_offset = 0.1
yyx_offset = 0.1
yyy_offset = 0.1
yxx_offset = 0.1
yxy_offset = 0.1

x1_pos = 100
x2_pos = 200
y1_pos = 100
y2_pos = 200

going_left = False
going_right = False
going_up = False
going_down = False

x = 100
y = 200
box_list = []


def init_game():
    pygame.display.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Project 1")

    glClearColor(0.0, 0.0, 0.0, 1.0)

def display():
    global box_list

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    # Rectangle - Bouncing
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(xxx_pos, xxy_pos)
    glVertex2f(xyx_pos, xyy_pos)
    glVertex2f(yyx_pos, yyy_pos)
    glVertex2f(yxx_pos, yxy_pos)
    glEnd()

    # Rectangle - Moveable
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x1_pos, y1_pos)
    glVertex2f(x1_pos, y2_pos)
    glVertex2f(x2_pos, y2_pos)
    glVertex2f(x2_pos, y1_pos)
    glEnd()

    for x in box_list:
        # new rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x[0], x[1] - 100)
        glVertex2f(x[0], x[1])
        glVertex2f(x[0] + 100, x[1])
        glVertex2f(x[0] + 100, x[1] - 100)
        glEnd()

    pygame.display.flip()

def bounce():
    global xxx_pos
    global xxy_pos
    global xyx_pos
    global xyy_pos
    global yyx_pos
    global yyy_pos
    global yxx_pos
    global yxy_pos

    global xxx_offset
    global xxy_offset
    global xyx_offset
    global xyy_offset
    global yyx_offset
    global yyy_offset
    global yxx_offset
    global yxy_offset

    # hits y top border
    if yyy_pos >= 600:
        xxy_offset = -0.1
        xyy_offset = -0.1
        yyy_offset = -0.1
        yxy_offset = -0.1

    # hits x right most border
    if yyx_pos >= 800:
        xxx_offset = -0.1
        xyx_offset = -0.1
        yyx_offset = -0.1
        yxx_offset = -0.1

    # hits y bottom border
    if xxy_pos <= 0:
        xxy_offset = 0.1
        xyy_offset = 0.1
        yyy_offset = 0.1
        yxy_offset = 0.1
    # hits x left most border
    if xxx_pos <= 0:
        xxx_offset = 0.1
        xyx_offset = 0.1
        yyx_offset = 0.1
        yxx_offset = 0.1

    xxx_pos += xxx_offset
    xxy_pos += xxy_offset

    xyx_pos += xyx_offset
    xyy_pos += xyy_offset

    yyx_pos += yyx_offset
    yyy_pos += yyy_offset

    yxx_pos += yxx_offset
    yxy_pos += yxy_offset


def game_loop():
    global going_left
    global going_right
    global going_up
    global going_down

    global x1_pos
    global x2_pos
    global y1_pos
    global y2_pos

    global x
    global y
    global box_list

    display()

    # bouncing box
    bounce()

    # movement with boarders
    if going_left:
        if x1_pos > 0:
            x1_pos -= 0.1
            x2_pos -= 0.1
    if going_right:
        if x2_pos < 800:
            x1_pos += 0.1
            x2_pos += 0.1
    if going_up:
        if y2_pos < 600:
            y1_pos += 0.1
            y2_pos += 0.1
    if going_down:
        if y1_pos > 0:
            y1_pos -= 0.1
            y2_pos -= 0.1

    for event in pygame.event.get():
        # trying to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # if a keyboard event happens (a key is pressed)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == K_LEFT:
                going_left = True
            elif event.key == K_RIGHT:
                going_right = True
            elif event.key == K_UP:
                going_up = True
            elif event.key == K_DOWN:
                going_down = True
        
        # key up event
        elif event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                going_left = False
            elif event.key == K_RIGHT:
                going_right = False
            elif event.key == K_UP:
                going_up = False
            elif event.key == K_DOWN:
                going_down = False

        # If a mousebutton click event happens 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(pygame.mouse.get_pos())
                if (pygame.mouse.get_pos()[0] - 50, 650 - pygame.mouse.get_pos()[1]) not in box_list:
                    box_list.append(
                        (pygame.mouse.get_pos()[0] - 50, 650 - pygame.mouse.get_pos()[1]))


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
