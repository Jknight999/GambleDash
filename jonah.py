import pygame
from time import sleep
import random


class Player:
    def __init__(self, sw, sh):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 50
        self.h = 50
        self.x = (self.SCREENWIDTH - self.w) / 2
        self.y = (self.SCREENHEIGHT - self.h) / 2
        self.color = (255, 0, 0)

    def apply_physics(self):
        if self.y < SCREENHEIGHT - self.h:
            self.y += 10


def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

SCREENWIDTH = 600
SCREENHEIGHT = 600
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
    player.apply_physics()
    #3. Draw New
    draw_player(player)
    #4. Update and Wait
    pygame.display.flip()
    sleep(0.02)