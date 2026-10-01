#imports
import pygame
import math

#player class
class Player:
    def __init__(self, sw, sh):
        #setting char properties
        self.scrw = sw
        self.scrh = sh
        self.w = 40
        self.h = 40
        self.x = 100
        self.y = 100
        self.color = (255, 0, 0)
        self.y_vel = 0
        self.gravity = 120
        self.jump_strength = -1600

    #player jump function, only called when jumping = 1
    def jump(self):
        self.y_vel = self.jump_strength

    #applies gravity and ground collision detection
    def apply_physics(self):
        global GROUND_Y
        self.y_vel += self.gravity
        self.y += self.y_vel * dt
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.y_vel = 0

#basic vars
SCREENWIDTH = 1000
SCREENHEIGHT = 600
GROUND_Y = math.floor(0.66*SCREENHEIGHT)
FRAMERATE = 120

#draws player to the screen
def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

def draw_screen(f_color):
    global GROUND_Y, SCREENHEIGHT
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, f_color, (0, GROUND_Y, SCREENWIDTH, math.ceil(0.34 * SCREENHEIGHT)))

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()
clock = pygame.time.Clock()
dt = 0
floor_color = [0, 102, 255]
running = True

#creates the player
player = Player(SCREENWIDTH, SCREENHEIGHT)

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
        if player.y >= GROUND_Y - player.h:
            player.y = GROUND_Y - player.h
            player.jump()
    player.apply_physics()

    #3. Draw New
    draw_screen(floor_color)
    draw_player(player)

    #4. Update and Wait
    dt = clock.tick(FRAMERATE) / 1000
    clock.tick(FRAMERATE)
    pygame.display.update()