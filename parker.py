import pygame
from time import sleep
import math
import random


class Player:
    def __init__(self, sw, sh):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 10
        self.h = 10
        self.x = (self.SCREENWIDTH - self.w) / 2
        self.y = (self.SCREENHEIGHT - self.h) / 2
        self.color = (255, 0, 0)


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

floor_y = math.floor(0.66 * SCREENHEIGHT)


def draw_screen(s_w, s_h, floor_color):
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, floor_color, (0, math.floor(0.66 * s_h), s_w, math.ceil(0.34 * s_h)))


SCREENWIDTH = 800
SCREENHEIGHT = 450

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

    #1. Erase Old
    screen.fill(0)
    #2. Make Changes
    ''''
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)
    '''

    #3. Draw New bozo
    draw_player(player)
    #4. Update and Wait
    pygame.display.flip()
    sleep(0.02)