import pygame
import pygame.freetype
import math
from time import sleep

class Player:
    #player characteristics
    def __init__(self, sw, sh, floor_y):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = SCREENWIDTH / 20
        self.h = SCREENHEIGHT / 10
        self.x = (self.SCREENWIDTH - self.w) / 5
        self.y = (floor_y - self.h)
        self.color = (14, 237, 70)
        self.y_vel = 0
        self.gravity = 1800000 / SCREENHEIGHT
        self.jump_strength = -900
        self.angle = 0
        self.rotation_speed = -(self.gravity / 10)

        #makes a sprite of the cube asset
        self.image = pygame.image.load("Assets/player_cube.png").convert_alpha()
        #sets the size to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        # draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def rotate_player(self):
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        # rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def jump(self):
        self.y_vel = self.jump_strength

    def apply_physics(self):
        #applies gravity and ground collision detection
        self.y_vel += self.gravity * dt
        self.y += self.y_vel * dt
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.y_vel = 0
            # snaps the cube back to flat on the ground
            self.angle = round(self.angle / 90) * 90 % 360
            self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

class Spike:
    #spike characteristics
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SCREENWIDTH / 20
        self.height = SCREENHEIGHT / 10
        self.speed = 550
        self.hitbox = pygame.Rect(x + self.width / 2.5, self.y + self.height / 3, self.width / 5, self.height / 2.3)

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        #needed because triangles drawn through draw.polygon()
        # These vertices should not be used for hitboxes, spike hitboxes are rectangular
        return [[self.x, self.y + self.height], [self.x + self.width / 2, self.y], [self.x + self.width, self.y + self.height]]

    def scroll(self):
        # moves spike from left to right side of screen
        self.x -= self.speed * dt
        self.hitbox = pygame.Rect(self.x + self.width / 2.5, self.y + self.height / 3, self.width / 5, self.height / 2.3)

    def check_collision(self):
        global running, in_game, player
        if player.rect.colliderect(self.hitbox):
            screen.fill((255, 0, 0))
            sleep(1)
            reset_game()


class Block:
    # spike characteristics
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SCREENWIDTH / 20
        self.height = SCREENHEIGHT / 10
        self.speed = 550
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

    def scroll(self):
        # moves spike from left to right side of screen
        self.x -= self.speed * dt
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

class Button:
    #takes in characteristics as arguments and makes a rect with them
    def __init__(self, x, y, w, h, color, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        #if the text argument is filled it will parse the tuple and change the font size to the specified num
        if text != 0:
            self.text, self.font_name, self.text_size, self.text_color = text
            self.font = pygame.freetype.Font(self.font_name, self.text_size)

    def render_text(self):
        #gets the rectangle that bounds the text
        text_rect = self.font.get_rect(self.text)
        #sets the center to the center of the button
        text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        #prints (renders) the text to the screen
        self.font.render_to(screen, text_rect, self.text, self.text_color)

    #draws the button
    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    #checks if the button is clicked and loads GambleDash
    def check_button_click(self, click_event, button_type):
        global in_game
        global in_casino
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1:
                if button_type == "Play":
                    in_game = True
                elif button_type == "Gamble":
                    in_casino = True

def draw_player(to_draw):
    global screen
    screen.blit(to_draw.rotated_surface, to_draw.rect)
    #pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

def draw_spike(to_draw):
    #creates a list of the spikes (so that it can be iterated through)
    #empty so that it can be filled with the vertices of each spike
    #spike_to_draw= [None] * amount
    global screen
    #giving myself the ability to separate the vertices
    v_a, v_b, v_c = to_draw.find_vertices()
    pygame.draw.polygon(screen, (0, 0, 0), (v_a, v_b, v_c))
    #shrinking the vertices inwards so that the outline doesn't go outside the block allotted
    v_a[0] += 5
    v_a[1] -= 3
    v_b[1] += 3
    v_c[0] -= 5
    v_c[1] -= 3
    pygame.draw.polygon(screen, (255, 255, 255), (v_a, v_b, v_c), width=3)
    if SHOW_SPIKE_HITBOXES:
        pygame.draw.rect(screen, (255, 0, 0), to_draw.hitbox, width=1)
    #loops once for each spike
    ''''
    for i in amount:
        #matches each spike to its vertices by passing in the spike number to the function, which returns its vertices
        spike_to_draw[i] = to_draw.find_vertices(i)
        pygame.draw.polygon(screen, (0, 0, 0), spike_to_draw[i])
        pygame.draw.polygon(screen, (255, 255, 255), spike_to_draw[i], width=3)
    '''

def draw_block(to_draw):
    global screen
    pygame.draw.rect(screen, (9, 30, 92), to_draw.block)

def draw_platformer_screen(floor):
    screen.fill((17, 56, 171))
    #calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))

def draw_menu_screen():
    screen.fill((17, 56, 171))
    play_button.draw_button(screen)
    play_button.render_text()
    casino_button.draw_button(screen)
    casino_button.render_text()

def draw_casino_screen():
    global casino_font
    screen.fill((94, 6, 6))
    CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 4), f'Your Chips: {chips}', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20))

def parse_level(level,tick):
    for row_number in range(len(level)):
         if level[row_number][tick] == '1':
             spikes.append(Spike(screen.get_width(), (SCREENHEIGHT / 10) * row_number))
         elif level[row_number][tick] == '0':
             print('Block!')
             blocks.append(Block(screen.get_width(), (SCREENHEIGHT / 10) * row_number))

def reset_game():
    global in_game, in_casino, player, spikes, blocks, tick_counter, frame_counter
    in_game = False
    in_casino = False
    player.__init__(SCREENWIDTH,SCREENHEIGHT,GROUND_Y)
    spikes = []
    blocks = []
    tick_counter = 0
    frame_counter = 0

#screen setup
FRAMERATE = 120
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * 0.5
SHOW_SPIKE_HITBOXES = True

#Text Stuff
pygame.freetype.init()
#default size
gd_font_size = 80
gd_font = pygame.freetype.Font("Assets/pusab.otf", gd_font_size)
#cache of common fonts in a dict - so to use the cached font its GD_FONTS[font_size]
#did this because changing the size of the fonts everytime took too much code and too long (runtime wise)
#normally to change it you would have to put gd_font = pygame.freetype.Font('Assets/pusab.otf', the size you wanted to change it to)
#not cached for buttons
GD_FONTS = {
    14: pygame.freetype.Font('Assets/pusab.otf', 14),
    18: pygame.freetype.Font('Assets/pusab.otf', 18),
    24: pygame.freetype.Font('Assets/pusab.otf', 24),
    32: pygame.freetype.Font('Assets/pusab.otf', 32),
    50: pygame.freetype.Font('Assets/pusab.otf', 50),
    100: pygame.freetype.Font('Assets/pusab.otf', 100)
}

#initializes the font with default size
casino_font_size = 100
casino_font = pygame.freetype.Font("Assets/casino.ttf", casino_font_size)
CASINO_FONTS = {
    14: pygame.freetype.Font('Assets/casino.ttf', 14),
    18: pygame.freetype.Font('Assets/casino.ttf', 18),
    24: pygame.freetype.Font('Assets/casino.ttf', 24),
    32: pygame.freetype.Font('Assets/casino.ttf', 32),
    50: pygame.freetype.Font('Assets/casino.ttf', 50),
    100: pygame.freetype.Font('Assets/casino.ttf', 100)
}

#where the top of the floor is (for collision physics principles)
GROUND_Y = math.floor(0.7 * SCREENHEIGHT)

#in a list, so IT CAN CHANGE
floor_color = [9, 30, 92]
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync = 1)
pygame.init()
clock =  pygame.time.Clock()

# New level data list
# 1 is a spike, 0 is a block, ' ' is nothing
levels = {
    1: (
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                        0                                              ',
    '                                                                       ',
    '                                       0                               ',
    '        111        1       1     1        111           11       1      '
    )
}

tick_counter = 0
frame_counter = 0

#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

#now takes a text argument - ('text', 'font file name', size, color(R,G,B))
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))

# lists of generated instances of the classes to allow for multiple to be on screen
spikes = []
blocks = []

# List of buttons that can be used to jump
jump_buttons = [pygame.K_w, pygame.K_SPACE]

pygame.display.set_caption("GambleDash")
chips= 100
dt = 0
running = True
in_game = False
in_casino = False
current_level = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                in_game = not in_game
        # sends event to button to see if it's been clicked
        play_button.check_button_click(event, "Play")
        casino_button.check_button_click(event, "Gamble")

    if in_game:
        # jumping if space bar is pressed, otherwise not
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if player.y >= GROUND_Y - player.h:
                player.y = GROUND_Y - player.h
                player.jump()
        player.apply_physics()
        #rotate player if they're in the air
        if player.y < GROUND_Y - player.h:
            player.rotate_player()
        for spike in spikes:
            spike.scroll()
        for block in blocks:
            block.scroll()
        if frame_counter % math.floor(SCREENWIDTH / 200) == 0:
            if tick_counter < len(levels[current_level][0]) - 1:
                tick_counter += 1
            else:
                tick_counter = 0
            parse_level(levels[current_level], tick_counter)
        frame_counter += 1
    else:
        pass

    if in_game:
        draw_platformer_screen(floor_color)
        draw_player(player)
        for k in spikes:
            draw_spike(k)
            k.check_collision()
        for k in blocks:
            draw_block(k)
    elif in_casino:
        draw_casino_screen()
    else:
        draw_menu_screen()

    #4. Update and Wait
    dt = clock.tick(FRAMERATE) / 1000
    pygame.display.flip()