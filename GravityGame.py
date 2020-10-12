import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random as ran
from random import *
from math import *
import time

clock = pygame.time.Clock()
display_width = 800
display_height = 600
mouse_pos = None
enemies = []

countdown = 5
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)

class Enemy:
    def __init__(self, etype, x, size, y, side):
        self.etype = etype
        self.x = x
        self.size = size 
        self.y = y
        self.side = side

        self.distance = None
        self.hit = False
        self.slope = None
        self.angle = None

    def draw(self):
        if self.etype == "rect":
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x, self.y + self.size)
            glVertex2f(self.x + self.size, self.y + self.size)
            glVertex2f(self.x + self.size, self.y)
            glEnd()
        if self.etype == "line":
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.size, self.y + self.size)
            glEnd()
        if self.etype == "tri":
            glBegin(GL_TRIANGLES)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x, self.y + self.size)
            glVertex2f(self.x + self.size, self.y + self.size)
            glEnd()
        if self.etype == "circle":
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(self.x, self.y)
            vert = 50
            for i in range(0, vert + 1):
                glVertex2f(
                    self.x + ((self.size/2) * cos(i *  (2* pi) / vert)), 
                    self.y + ((self.size/2) * sin(i * (2* pi)  / vert))
                    )
            glEnd()

    def get_pointers(self, dist_x, dist_y):
        if (self.etype =="circle"):
            xpoint = dist_x - self.x
            ypoint = dist_y - self.y
        else:
            if (self.side == 3 or self.side == 0) and (self.x < dist_x and self.y <= dist_y):
                xpoint = dist_x - (self.x + self.size)
                ypoint = dist_y - (self.y + self.size)
            elif (self.side == 0 or self.side == 1) and (self.x <= dist_x and self.y > dist_y):
                if self.etype == "rect":
                    xpoint = dist_x - (self.x + self.size)
                    ypoint = dist_y - self.y
                else:
                    xpoint = dist_x - self.x
                    ypoint = dist_y - self.y 
            elif (self.side == 1 or self.side == 2) and (self.x > dist_x and self.y >= dist_y):
                xpoint = dist_x - self.x
                ypoint = dist_y - self.y
            elif (self.side == 2 or self.side == 3) and (self.x >= dist_x and self.y < dist_y):
                if self.etype == "rect" or self.etype == "tri":
                    xpoint = dist_x - self.x
                    ypoint = dist_y - (self.y + self.size)
                else:
                    xpoint = dist_x - self.x
                    ypoint = dist_y - self.y  
            else:
                xpoint = dist_x - self.x
                ypoint = dist_y - self.y 
        return xpoint, ypoint

    def move(self):
        global mouse_pos
        global display_height

        xp, yp = self.get_pointers(mouse_pos[0], display_height - mouse_pos[1])
        mouse_dist = sqrt(xp**2 + yp**2)

        # are we being hit?
        if ((self.etype == "circle") and (mouse_dist <= 10 + (self.size/2))):
            self.enemy_hit()

        if (mouse_dist <= 10):
            self.enemy_hit()

        # we are not being hit
        elif not self.hit:
            xpoint, ypoint = self.get_pointers(400, 300)        
            self.distance = sqrt(xpoint**2 + ypoint**2)

            if self.etype == "circle":
                self.distance -= (self.size/2)

            self.angle = atan(ypoint/xpoint) + 360
            self.slope = ypoint/xpoint

            self.x += xpoint/100
            self.y += ypoint/100

    def is_hit(self):
        return self.hit
    
    def enemy_hit(self): 
        self.hit = True

        n = (self.y * - 1, self.x)
        r = self.y + (self.slope * -1 * self.x)
        c = (self.slope, r)

        above_d = ((c[0] * n[0]) + (c[1] * n[1])) * 2
        below_d = ((n[0] * n[0]) + (n[1] * n[1]))

        d = above_d/below_d
        v = (d * n[0], d * n[1])

        new_direction = (c[0] - v[0], c[1] - v[1])

        # this seems not to be working correctly, tried to use reflection 

        # self.x += new_direction[0] / self.distance
        # self.y += new_direction[1] / self.distance

        self.x += n[0] / self.distance
        self.y += n[1] / self.distance

    def out_of_bounds(self):
        # is enemy out of bounds, then we need to delete
        return self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600


def init_game():
    global display_width
    global display_height

    pygame.display.init()
    pygame.font.init()
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Project 2")

    glClearColor(0.0, 0.0, 0.0, 1.0)

def display():
    global display_width
    global display_height
    global mouse_pos

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    # draw main circle
    draw_circle(x=display_width/2, y=display_height/2, rad=50)

    # draw mousepointer cirlce
    if mouse_pos != None:
        draw_circle(x=mouse_pos[0], y=display_height - mouse_pos[1], rad=10)

    # draw enemies 
    for x in enemies:
        x.draw()
        # move towards
        if not x.is_hit():
            if (x.distance == None or x.distance > 52):
                x.move()
            else:
                defeat()
        # move away
        else:
            x.enemy_hit()
            if x.out_of_bounds():
                remove_enemy(x)
        
    pygame.display.flip()

def remove_enemy(e):
    global enemies
    enemies.remove(e)


def defeat():
    global display_width
    global display_height

    pygame.display.flip()

    # setting font settings 
    game_display = pygame.display.set_mode((display_width,display_height))
    font_settings = pygame.font.SysFont("calibri",30)
    text = font_settings.render("You have failed to defend the circle!", True, (255,255,255))

    text_rect = text.get_rect()
    text_rect.center = ((display_width/2),(display_height/2))

    game_display.blit(text, text_rect)
    pygame.display.update()

    time.sleep(2)

def enemy_generator():
    global enemies
    global countdown
    global display_width
    global display_height

    rand = ran.randrange(0, 800, 30)
    side = ran.randrange(0, 4)
    shape = ran.choice(["rect", "line", "tri", "circle"])

    size = ran.randrange(20, 50)

    # set variables depending on what side enemy comes from
    if side == 0:
        if shape == "rect":
            enemies.append(Enemy("rect", 0, size, rand % 600, side))
        if shape == "line":
            enemies.append(Enemy("line", 0, size, rand % 600, side))
        if shape == "tri":
            enemies.append(Enemy("tri", 0, size, rand % 600, side))
        if shape == "circle":
            enemies.append(Enemy("circle", 0, size, rand % 600, side))

    if side == 1:
        if shape == "rect":
            enemies.append(Enemy("rect", rand, size, display_height, side))
        if shape == "line":
            enemies.append(Enemy("line", rand, size, display_height, side))
        if shape == "tri":
            enemies.append(Enemy("tri", rand, size, display_height, side))
        if shape == "circle":
            enemies.append(Enemy("circle", rand, size, display_height, side))
            
    if side == 2:
        if shape == "rect":
            enemies.append(Enemy("rect", display_width, size, rand % 600, side))
        if shape == "line":
            enemies.append(Enemy("line", display_width, size, rand % 600, side))
        if shape == "tri":
            enemies.append(Enemy("tri", display_width, size, rand % 600, side))
        if shape == "circle":
            enemies.append(Enemy("circle", display_width, size, rand % 600, side))

    if side == 3:
        if shape == "rect":
            enemies.append(Enemy("rect", rand, size, 0, side))
        if shape == "line":
            enemies.append(Enemy("line", rand, size, 0, side))
        if shape == "tri":
            enemies.append(Enemy("tri", rand, size, 0, side))
        if shape == "circle":
            enemies.append(Enemy("circle", rand, size, 0, side))


def draw_circle(x, y, rad):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    vert = 50

    for i in range(0, vert + 1):
        glVertex2f(
            x + (rad * cos(i *  (2* pi) / vert)), 
            y + (rad * sin(i * (2* pi)  / vert))
            )

    glEnd()

def game_loop():
    global mouse_pos
    global timer_event
    global countdown
    global sec

    display()

    # event handler
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

        # moving defendant
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

        # our timer 
        elif event.type == timer_event:
            countdown -= 1
            print(countdown)
            if countdown == 0:
                # create new enemy
                enemy_generator()
                # start countdown again
                countdown = 3
                timer_event = pygame.USEREVENT+1
                pygame.time.set_timer(timer_event, 1000)

if __name__ == "__main__":

    init_game()
    while True:
        game_loop()
        clock.tick(60)

