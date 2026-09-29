#imports
import pygame
from time import sleep
import math
import random

#player class
class Player:
    def __init__(self, sw, sh):
        #setting char properties
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 20
        self.h = 20
        self.x = (self.SCREENWIDTH - self.w) / 2
        self.y = (self.SCREENHEIGHT - self.h) / 2
        self.color = (255, 0, 0)
        self.y_vel = 0
        self.gravity = 0.8
        self.jump_strength = -12

    #player jump function, only called when jumping = 1
    def jump(self):
        pass

#draws player to the screen
def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

SCREENWIDTH = 600
SCREENHEIGHT = 600

def draw_screen(sw, sh, floor_color):
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, floor_color, (0, math.floor(0.66*sh), sw, math.ceil(0.34 * sh)))
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

#creates the player
player = Player(SCREENWIDTH, SCREENHEIGHT)
floor_color = [0, 102, 255]
running = True
jumping = 0

while running:
    #1. Erase Old
    screen.fill(0)
    #2. Make Changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #jumping if space bar is pressed, otherwise not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumping = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jumping = 0
    #calls jump function if space bar is pushed
    if jumping:
        player.jump()
    #3. Draw New
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)
    draw_player(player)

    #4. Update and Wait
    pygame.display.update()
    sleep(0.02)