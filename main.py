# COMMENT YOUR FUCKING CODE
# As we add more stuff it will become less readable
import pygame
from time import sleep
import random
import math

FRAMERATE = 80

class Player:
    def __init__(self, sw, sh, floor_y):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 40
        self.h = 40
        self.x = (self.SCREENWIDTH - self.w) / 5
        self.y = (floor_y - self.h)
        self.color = (0, 200, 0)
        self.y_vel = 0
        self.gravity = 1.5
        self.jump_strength = -20

    def jump(self):
        self.y_vel = self.jump_strength

    def apply_physics(self):
        self.y_vel += player.gravity
        self.y += player.y_vel

        if player.y >= math.ceil(floor_y - self.h):
            self.y = math.ceil(floor_y - self.h)
            self.y_vel = 0

class Spike:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 15

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        #needed because triangles drawn through draw.polygon()
        # These vertices should not be used for hitboxes, spike hitboxes are rectangular
        return [[self.x - self.width/2, self.y], [self.x, self.y - self.height], [self.x + self.width/2, self.y]]

    def scroll(self):
        # moves spike from left to right side of screen, and loops it back to right
        self.x -= self.speed
        if self.x < 0:
            self.__init__(screen.get_width() - 50, floor_y)

def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

def draw_spike(to_draw):
    global screen
    pygame.draw.polygon(screen, (255, 255, 255), to_draw.find_vertices())


def draw_screen(s_w, s_h, floor_color):
    screen.fill((0, 0, 102))
    #calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor_color, (0, math.floor(0.66 * s_h), s_w, math.ceil(0.34 * s_h)))

#16:9 aspect ratio
SCREENWIDTH = 800
SCREENHEIGHT = 450

#where the top of the floor is (for collision physics principles)
floor_y = math.floor(0.66 * SCREENHEIGHT)

#in a list, so IT CAN CHANGE
floor_color = [0, 102, 255]
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, floor_y)
spike = Spike(screen.get_width() - 50, floor_y)

running = True
jumping = 0
while running:
    # Clear screen
    draw_screen(SCREENWIDTH, SCREENHEIGHT, floor_color)

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

    # Coded in this way to allow for holding jump
    if jumping and player.y == math.ceil(floor_y - player.h):
        player.jump()

    player.apply_physics()
    spike.scroll()

    #3. Draw New
    draw_player(player)
    draw_spike(spike)

    #4. Update and Wait
    sleep(1/FRAMERATE)
    pygame.display.flip()