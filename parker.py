import pygame
from time import sleep
import math
import random


class Player:
    def __init__(self, sw, sh):
        #setting char properties
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 40
        self.h = 40
        self.x = (self.SCREENWIDTH - self.w) / 5
        self.y = (self.SCREENHEIGHT - self.h) / 2
        self.color = (255, 0, 0)
        self.y_vel = 0
        self.y_term_vel = 3
        self.gravity = 0.1
        self.jump_strength = -12

    def apply_physics(self):
        if self.y_vel < -self.y_term_vel:
            self.y_vel = -self.y_term_vel
        self.y_vel -= self.gravity
        if self.y > floor_y - self.h:
            self.y -= self.y_vel
        if self.y < floor_y - self.h:
            self.y = floor_y - self.h
            self.y_vel = 0

    #player jump function, only called when jumping = 1
    def jump(self):
        self.y = 100


def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

'''
def draw_screen(s_w, s_h, floor_color):
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, floor_color, (0, math.floor(0.66 * s_h), s_w, math.ceil(0.34 * s_h)))
    
SCREENWIDTH = 800
SCREENHEIGHT = 450

floor_y = math.floor(0.66 * SCREENHEIGHT)

floor_color = [0, 102, 255]
'''

def draw_screen(s_w, s_h, floor_color):
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, floor_color, (0, math.floor(0.66 * s_h), s_w, math.ceil(0.34 * s_h)))


SCREENWIDTH = 800
SCREENHEIGHT = 450

floor_y = math.floor(0.66 * SCREENHEIGHT)

floor_color = [0, 102, 255]

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()
pygame.display.update()

player = Player(SCREENWIDTH, SCREENHEIGHT)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumping = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jumping = 0

    #1. Erase Old
    screen.fill(0)
    #2. Make Changes
    player.apply_physics()
    ''''
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)
    '''
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)


    #3. Draw New bozo
    draw_player(player)
    #4. Update and Wait
    pygame.display.flip()
    sleep(0.02)