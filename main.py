# COMMENT YOUR F***ING CODE
# As we add more stuff it will become less readable
# Also MULTIPLY ALL MOVEMENT BY "dt". dt stands for delta time
# and makes physics independent of framerate.
import pygame
import math

FRAMERATE = 120
SCREENWIDTH = 800
SCREENHEIGHT = SCREENWIDTH * 9 / 16
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync = 1)
pygame.init()
clock =  pygame.time.Clock()

player_sprite = pygame.image.load("Assets/player_cube.png").convert()
player_sprite = pygame.transform.scale(player_sprite, (40,40))
class Player:
    def __init__(self, sw, sh, floor_y):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = 40
        self.h = 40
        self.x = (self.SCREENWIDTH - self.w) / 5
        self.y = (floor_y - self.h)
        self.color = (14, 237, 70)
        self.y_vel = 0
        self.gravity = 15000
        self.jump_strength = -1600
        self.angle = 0
        self.rotation_speed = -7
        # makes a transparent surface
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        # makes a copy of the surface that will be rotated from the original surface by the turn angle
        self.rotated_surface = self.surface
        # draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def rotate_player(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        # rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def jump(self):
        self.y_vel = self.jump_strength

    def apply_physics(self):
        self.y_vel += self.gravity * dt
        self.y += self.y_vel * dt
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.y_vel = 0
            # snaps the cube back to flat on the ground
            self.angle = round(self.angle / 90) * 90 % 360
            self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

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
        # moves spike from left to right side of screen
        self.x -= self.speed * dt

class Button:
    #takes in characteristics as arguments and makes a rectangle with them
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    #draws the button
    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    #checks if the button is clicked and loads GambleDash
    def check_button_click(self, click_event):
        global in_game
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if click_event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                in_game = True

def draw_player(to_draw):
    global screen
    screen.blit(player_sprite, to_draw.rect)
    #pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

def draw_spike(to_draw, amount):
    #creates a list of the spikes (so that it can be iterated through)
    #empty so that it can be filled with the vertices of each spike
    spike_to_draw = [None] * len(amount)
    global screen
    #loops once for each spike
    for i in amount:
        #matches each spike to its vertices by passing in the spike number to the function, which returns its vertices
        spike_to_draw[i] = to_draw.find_vertices(i)
        pygame.draw.polygon(screen, (0, 0, 0), spike_to_draw[i])
        pygame.draw.polygon(screen, (255, 255, 255), spike_to_draw[i], width=3)

def draw_platformer_screen(floor):
    screen.fill((17, 56, 171))
    #calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor, (0, GROUND_Y, SCREENWIDTH, math.ceil(0.34 * SCREENHEIGHT)))

#draws menu screen
def draw_menu_screen():
    screen.fill((17, 56, 171))
    play_button.draw_button(screen)

# Takes the list of level data and puts a spike on 1s
def parse_level(level,tick):
    if level[tick] == 1:
        spikes.append(Spike(screen.get_width() - 50, GROUND_Y, 1))


#where the top of the floor is (for collision physics principles)
GROUND_Y = math.floor(0.66 * SCREENHEIGHT)

#in a list, so IT CAN CHANGE
floor_color = [9, 30, 92]


# New level data list
# 1 is a spike, 0 is nothing
# Mess around and see if you can make something cool
#could you possibly edit the construction of the list using the * string operator so that you just do '0' * 6, '1' * 3...
level_1 = [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
tick_counter = 0
frame_counter = 0
#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)
play_button = Button(SCREENWIDTH / 2 - SCREENWIDTH / 8, SCREENHEIGHT / 2 - SCREENHEIGHT / 8, SCREENWIDTH / 4, SCREENHEIGHT / 4, (14, 237, 70))
# Allows multiple spikes to be on screen now
spikes = []

# List of buttons that can be used to jump
jump_buttons = [pygame.K_w, pygame.K_SPACE]

dt = 0
running = True
in_game = False
jumping = 0
while running:
    #2. Make Changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                in_game = not in_game
        # sends event to button to see if it's been clicked
        play_button.check_button_click(event)

    if in_game:
        # jumping if space bar is pressed, otherwise not
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if player.y >= GROUND_Y - player.h:
                player.y = GROUND_Y - player.h
                player.jump()
        player.apply_physics()
        if player.y < GROUND_Y - player.h:
            player.rotate_player()
        for k in spikes:
            k.scroll()
        if frame_counter % 4 == 0:
            if tick_counter < len(level_1) - 1:
                tick_counter += 1
            else:
                tick_counter = 0
            parse_level(level_1, tick_counter)
        frame_counter += 1
    else:
        pass

    if in_game:
        draw_platformer_screen(floor_color)
        draw_player(player)
        for k in spikes:
            draw_spike(k, k.amount)
    else:
        draw_menu_screen()

    #4. Update and Wait
    dt = clock.tick(FRAMERATE) / 1000
    clock.tick(FRAMERATE)
    pygame.display.flip()