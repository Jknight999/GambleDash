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
        self.y_vel = self.jump_strength

#draws player to the screen
def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

SCREENWIDTH = 600
SCREENHEIGHT = 600

def draw_screen(sw, sh, f_color):
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, f_color, (0, math.floor(0.66*sh), sw, math.ceil(0.34 * sh)))
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

#creates the player
player = Player(SCREENWIDTH, SCREENHEIGHT)
floor_color = [0, 102, 255]
running = True

#why 0 instead of False? since it will only be True or False? I guess it's the same thing
jumping = 0

while running:
    #1. Erase Old
    screen.fill(0)
    #2. Make Changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #jumping if space bar is pressed, otherwise not


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if player.y >= math.ceil(0.66 * SCREENHEIGHT) - player.h:
            player.y = math.ceil(0.66 * SCREENHEIGHT) - player.h
            player.jump()

    #calls jump function if space bar is pushed
    if jumping:
        print("Jump")
    player.y_vel += player.gravity
    player.y += player.y_vel


    if player.y >= math.ceil(0.66 * SCREENHEIGHT) - player.h:
        player.y = math.ceil(0.66 * SCREENHEIGHT) - player.h
        player.y_vel = 0
    #3. Draw New
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)
    draw_player(player)

    #4. Update and Wait
    pygame.display.update()
    sleep(0.02)