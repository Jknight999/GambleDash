# COMMENT YOUR F***ING CODE
# As we add more stuff it will become less readable
# Also MULTIPLY ALL MOVEMENT BY "dt". dt stands for delta time
# and makes physics independent of framerate.
import pygame
import random
import math

FRAMERATE = 120

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
        self.gravity = 120
        self.jump_strength = -1600

    def jump(self):
        self.y_vel = self.jump_strength

    def apply_physics(self):
        self.y_vel += self.gravity
        self.y += self.y_vel * dt

        if player.y >= math.ceil(floor_y - self.h):
            self.y = math.ceil(floor_y - self.h)
            self.y_vel = 0

class Spike:
    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 1200
        self.amount = [i for i in range(amount)]

    def find_vertices(self, spike_number):
        #calculates where the vertices should be based off x, y, w and h of the spike
        #needed because triangles drawn through draw.polygon()
        # These vertices should not be used for hitboxes, spike hitboxes are rectangular
        return [[self.x - self.width/2 + spike_number * self.width, self.y], [self.x + spike_number * self.width, self.y - self.height], [self.x + self.width/2 + spike_number * self.width, self.y]]

    def scroll(self):
        # moves spike from left to right side of screen, and loops it back to right
        self.x -= self.speed * dt
        if self.x < 0:
            self.__init__(screen.get_width() - 50, floor_y, random.randint(1, 3))

def draw_player(to_draw):
    global screen
    pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

def draw_spike(to_draw, amount):
    #creates a list of the spikes (so that it can be iterated through)
    #empty so that it can be filled with the vertices of each spike
    spike_to_draw = [None] * len(amount)
    global screen
    #loops once for each spike
    for i in amount:
        #matches each spike to its vertices by passing in the spike number to the function, which returns its vertices
        spike_to_draw[i] = to_draw.find_vertices(i)
        pygame.draw.polygon(screen, (255, 255, 255), spike_to_draw[i])


def draw_screen(s_w, s_h, floor):
    screen.fill((0, 0, 102))
    #calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor, (0, math.floor(0.66 * s_h), s_w, math.ceil(0.34 * s_h)))

#16:9 aspect ratio
screen_sizes = ('small', 'big', 's', 'b')
screen_size = input("small or big screen (s/b)")
while screen_size not in screen_sizes: screen_size = input("small or big screen (s/b)")
if screen_size == 'small' or screen_size == 's':
    SCREENWIDTH = 800
    SCREENHEIGHT = 450
else:
    SCREENWIDTH = 1600
    SCREENHEIGHT = 900

#where the top of the floor is (for collision physics principles)
floor_y = math.floor(0.66 * SCREENHEIGHT)

#in a list, so IT CAN CHANGE
floor_color = [0, 102, 255]
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync = 1)
pygame.init()
clock =  pygame.time.Clock()


#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, floor_y)
spike = Spike(screen.get_width() - 50, floor_y, random.randint(1, 3))

# List of buttons that can be used to jump
jump_buttons = [pygame.K_w, pygame.K_SPACE]

dt = 0
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
            if event.key in jump_buttons:
                jumping = 1
        if event.type == pygame.KEYUP:
            if event.key in jump_buttons:
                jumping = 0

    # Coded in this way to allow for holding jump
    if jumping and player.y == math.ceil(floor_y - player.h):
        player.jump()

    player.apply_physics()
    spike.scroll()

    #3. Draw New
    draw_player(player)
    #new argument needs to be passed in - the amount of spikes wanted
    draw_spike(spike, spike.amount)

    #4. Update and Wait
    dt = clock.tick(FRAMERATE) / 1000
    clock.tick(FRAMERATE)
    pygame.display.flip()