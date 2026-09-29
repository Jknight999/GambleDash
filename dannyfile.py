import pygame
from time import sleep
import random


class Player:
    def __init__(self, sw, sh):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 20
        self.h = 20
        self.x = (self.SCREENWIDTH - self.w) / 2
        self.y = (self.SCREENHEIGHT - self.h) / 2
        self.color = (255, 0, 0)
        self.x_vel = 10
        self.y_vel = 10

    def jump(self):
        pass

def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

SCREENWIDTH = 600
SCREENHEIGHT = 600
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

player = Player(SCREENWIDTH, SCREENHEIGHT)

running = True
jumping = 0

while running:
    #1. Erase Old
    screen.fill(0)
    #2. Make Changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumping = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jumping = 0
    if jumping:
        player.jump()
    #3. Draw New
    draw_player(player)

    #4. Update and Wait
    pygame.display.update()
    sleep(0.02)