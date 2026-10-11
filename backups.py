#Main Backup
'''
import pygame
import pygame.freetype
import math
from game_classes import Player, Button
from game_screen_manager import GameScreenManager

def draw_menu_screen():
    screen.fill((17, 56, 171))
    play_button.draw_button(screen)
    play_button.render_text(screen)
    casino_button.draw_button(screen)
    casino_button.render_text(screen)

def draw_casino_screen():
    global casino_font
    screen.fill((94, 6, 6))
    CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 4), f'Your Chips: {chips}', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20))
    back_button.draw_button(screen)
    back_button.render_text(screen)
    higher_or_lower_button.draw_button(screen)
    higher_or_lower_button.render_text(screen)

def draw_game_screen():
    screen.blit(bg)
    # calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor_color, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))
    #draws the back button to the screen
    back_button.draw_button(screen)
    back_button.render_text(screen)


#screen setup
FRAMERATE = 120
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * 0.5
SHOW_SPIKE_HITBOXES = False

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

bg = pygame.image.load("assets/background.jpg").convert()

#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

# I have absolutely no idea why but this is necessary to make the cube start the right way up
player.angle = 91
player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
player.rect = player.rotated_surface.get_rect(center=(player.x + player.w // 2, player.y + player.h // 2))

#now takes a text argument - ('text', 'font file name', size, color(R,G,B))
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), ('X', "Assets/pusab.otf", SCREENHEIGHT / 20, (245, 200, 76)))
higher_or_lower_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), ('Higher or Lower', 'Assets/casino.ttf', 40, (0, 0, 0)))

game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, FRAMERATE, pygame.time.Clock(), GROUND_Y, bg)
pygame.display.set_caption("GambleDash")
chips= 100
dt = 0
running = True
in_menu = True
in_game = False
in_casino = False
current_level = 1
while running:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # sends event to button to see if it's been clicked
        if in_menu:
            if play_button.check_button_click(event):
                in_menu = False
                in_game = True
            if casino_button.check_button_click(event):
                in_menu = False
                in_casino = True
        elif in_casino:
            if back_button.check_button_click(event):
                in_casino = False
                in_menu = True
        elif in_game:
            if back_button.check_button_click(event):
                in_game = False
                in_menu = True

    if in_game:
        draw_game_screen()
        game_screen.tick(player)
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()

    pygame.display.flip()
    '''

#Game Classes Backup
'''
import pygame
import pygame.freetype

class Player:
    #basic player characteristics
    def __init__(self, sw, sh, floor_y):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = self.SCREENWIDTH / 20
        self.h = self.SCREENHEIGHT / 10
        self.x = (self.SCREENWIDTH - self.w) / 4
        self.y = (floor_y - self.h)
        self.color = (14, 237, 70)
        self.y_vel = 0
        self.gravity = 1800000 / self.SCREENHEIGHT
        self.jump_strength = -900
        self.angle = 0
        self.rotation_speed = -(self.gravity / 10)

        #makes a sprite of the cube asset
        self.image = pygame.image.load("Assets/playerskin02.png").convert_alpha()
        #sets the size of the sprite to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        #draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        #creates a mask around the player for collision handling
        self.mask = pygame.mask.from_surface(self.rotated_surface)

    def rotate_player(self, dt):
        #calculates and sets rotation angle
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        #rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        self.mask = pygame.mask.from_surface(self.rotated_surface)

    def snap_rotation(self):
        self.angle = round(self.angle / 90) * 90 % 360
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x+self.w // 2, self.y + self.h // 2))
        self.mask = pygame.mask.from_surface(self.rotated_surface)

class Spike:
    #basic spike characteristics
    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10
        self.hitbox = pygame.Rect(x + self.width / 2.5, self.y + self.height / 3, self.width / 5, self.height / 2.3)

        #makes the spike hitbox into a surface
        self.surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)

        #makes the hitbox not transparent so a mask can be made around it
        self.surface.fill((255, 0, 0))

        #draws a mask around the surface
        self.mask = pygame.mask.from_surface(self.surface)

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        return [[self.x, self.y + self.height], [self.x + self.width / 2, self.y], [self.x + self.width, self.y + self.height]]

class Block:
    # Shared resources: create these only once.
    shared_image = None
    shared_mask = None
    shared_size = None

    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10

        size = (round(self.width), round(self.height))

        # Load, scale, and mask the image only once per size.
        if Block.shared_image is None or Block.shared_size != size:
            Block.shared_image = pygame.image.load("Assets/gambledashblock.png").convert_alpha()

            Block.shared_image = pygame.transform.scale(Block.shared_image, size)

            Block.shared_mask = pygame.mask.from_surface(Block.shared_image)
            Block.shared_size = size

        # Reuse the shared image and mask.
        self.image = Block.shared_image
        self.mask = Block.shared_mask

        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

        self.colliding = False

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

    def render_text(self, surface):
        #gets the rectangle that bounds the text
        text_rect = self.font.get_rect(self.text)
        #sets the center to the center of the button
        text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        #prints (renders) the text to the screen
        self.font.render_to(surface, text_rect, self.text, self.text_color)

    #draws the button
    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    #checks if the button is clicked
    def check_button_click(self, click_event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1:
            return True
        else:
            return False
'''

#Game Screen Manager Backup
'''
import random
from game_classes import Spike, Block
import math
import pygame
from structures import structure_dictionary

class GameScreenManager:
    #basic characteristics
    def __init__(self, screen_to_draw, current_player, s_w, s_h, fl_color, f_r, clock, f_y, bg):
        self.surface = screen_to_draw
        self.screen_width = s_w
        self.screen_height = s_h
        self.f_c = fl_color
        self.floor_y = f_y
        self.framerate = f_r
        self.player = current_player
        self.spikes = []
        self.blocks = []
        self.buttons = []
        self.scroll_speed = 550
        self.clock = clock
        self.tick_counter = 0
        self.frame_counter = 0
        self.dt = 0
        self.background = bg
        self.previous_player_bottom = current_player.y + current_player.h
        #all possible structures
        self.structures = structure_dictionary

        self.current_structure = random.randint(1, len(structure_dictionary))
        #returns tuple of if the player is colliding with a block
        self.colliding_with_block = False
        self.colliding_with = None

    def scroll(self):
        #scrolls spike and places hitbox
        for spike in self.spikes:
            spike.x -= self.scroll_speed * self.dt
            spike.hitbox.x = spike.x + spike.width / 2.5
        #scrolls block and block mask
        for block in self.blocks:
            block.x -= self.scroll_speed * self.dt
            block.block.x = block.x
        self.discard_objects()

    def discard_objects(self):
        remaining_spikes = []
        for spike in self.spikes:
            if spike.x + spike.width >= 0:
                remaining_spikes.append(spike)
        self.spikes = remaining_spikes

        remaining_blocks = []
        for block in self.blocks:
            if block.x + block.width >= 0:
                remaining_blocks.append(block)
        self.blocks = remaining_blocks

    def print_level(self, level, tick):
        #goes through each item in the structures list
        for row_number in range(len(level)):
            #if it is a 1 then makes a spike
            if level[row_number][tick] == '1':
                self.spikes.append(Spike(self.screen_width, (self.screen_height / 10) * row_number, self.screen_width, self.screen_height))
            #if it is a 0 then makes a block
            elif level[row_number][tick] == '0':
                self.blocks.append(Block(self.screen_width, (self.screen_height / 10) * row_number, self.screen_width, self.screen_height))

    def tick(self, current_player):
        # calculates delta time from framerate

        self.dt = self.clock.tick(self.framerate) / 1000

        #converts the tuple into two variables to work with throughout the code
        #scrolls the whole level
        self.scroll()

        # counts frames and converts into ticks
        if self.frame_counter % math.floor(self.screen_width / 200) == 0:
            if self.tick_counter < len(self.structures[self.current_structure][0]) - 1:
                self.tick_counter += 1
            else:
                self.tick_counter = 0
                temp = self.current_structure
                while temp == self.current_structure:
                    self.current_structure = random.randint(1, len(structure_dictionary))
                print(self.current_structure)
            self.print_level(self.structures[self.current_structure], self.tick_counter)
        self.frame_counter += 1

        #draws the game screen and the objects contained
        self.draw_objects()

        self.apply_physics(current_player)

        # rotates the player if they're in the air
        if current_player.y_vel != 0 and not self.colliding_with_block:
            current_player.rotate_player(self.dt)

        # checks spike and block collisions
        for k in self.spikes:
            self.check_spike_player_collision(k, current_player)
        self.colliding_with_block = False
        for k in self.blocks:
            # checks for each block if they are colliding with the player using colliderect()
            if (current_player.rect.colliderect(k.block) or k.y == current_player.rect.bottom) and k.x - k.width < current_player.x < k.x + k.width:
                # if they are, add the block that is to the variable that tracks it
                self.colliding_with = k
                # check to see if it is from the top or from the left
                self.check_block_player_collision(k, current_player, current_player.y_vel)
                # only one will be colliding, so you can break after one
                break

        # keeps the player above the floor
        self.check_ground_collisions(current_player)

        # checks for jumping every tick and applies gravity
        self.check_jump(current_player)

        # draws the player to the screen
        self.surface.blit(current_player.rotated_surface, current_player.rect)

    def check_jump(self, current_player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            # touching a block
            if self.colliding_with_block:
                current_player.y = self.colliding_with.y - current_player.h
                current_player.y_vel = current_player.jump_strength

            # touching the ground
            if current_player.y >= self.floor_y - current_player.h:
                current_player.y = self.floor_y - current_player.h
                current_player.y_vel = current_player.jump_strength

    def apply_physics(self, current_player):
        # applies gravity and ground collision detection
        current_player.y_vel += current_player.gravity * self.dt
        current_player.y += current_player.y_vel * self.dt

    def check_ground_collisions(self, current_player):
        #checks if the player is on the ground
        if current_player.y >= self.floor_y - current_player.h:
            current_player.y = self.floor_y - current_player.h
            current_player.y_vel = 0

            # snaps the cube back to flat on the ground
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)
        current_player.rect = current_player.rotated_surface.get_rect(center=(current_player.x + current_player.w // 2, current_player.y + current_player.h // 2))

    def check_block_player_collision(self, blk, current_player, current_player_yv):
        # if the player hits the side of the block then reset the game
        # checks if the y velocity is less than or equal to 0, or it's way below the block
        offset_x = int(blk.block.x - current_player.rect.x)
        offset_y = int(blk.block.y - current_player.rect.y)

        if ((current_player_yv <= 0 or current_player.y >= blk.y) and current_player.mask.overlap(blk.mask, (offset_x, offset_y))) and not current_player.rect.bottom == blk.y:
            self.surface.fill((0, 0, 0))
            self.reset_game(current_player)
            return
        elif current_player_yv > 0:
            # sets the tracking bool to true and resets the rect
            self.colliding_with_block = True
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)
            current_player.y = blk.block.y - current_player.h
            current_player.y_vel = 0
            current_player.rect = current_player.rotated_surface.get_rect(center=(current_player.x + current_player.w // 2, current_player.y + current_player.h // 2))

    def check_spike_player_collision(self, spk, current_player):
        # finds offset amount from the hitbox to the player
        offset_x = int(spk.hitbox.x - current_player.rect.x)
        offset_y = int(spk.hitbox.y - current_player.rect.y)

        # if the player and mask overlap then reset the level
        if current_player.mask.overlap(spk.mask, (offset_x, offset_y)):
            self.surface.fill((0, 0, 0))
            self.reset_game(current_player)


    def draw_objects(self):
        for to_draw in self.spikes:
            # giving myself the ability to separate the vertices
            v_a, v_b, v_c = to_draw.find_vertices()
            pygame.draw.polygon(self.surface, (0, 0, 0), (v_a, v_b, v_c))

            # shrinking the vertices inwards so that the outline doesn't go outside the block allotted
            v_a[0] += 5
            v_a[1] -= 3
            v_b[1] += 3
            v_c[0] -= 5
            v_c[1] -= 3
            pygame.draw.polygon(self.surface, (255, 255, 255), (v_a, v_b, v_c), width=3)

        #draws blocks to the screen
        for to_draw in self.blocks:
            self.surface.blit(to_draw.image, to_draw.block)

    #resets the game
    def reset_game(self, current_player):
        current_player.__init__(self.screen_width, self.screen_height, self.floor_y)
        self.spikes = []
        self.blocks = []
        self.tick_counter = 0
        self.frame_counter = 0
'''

#Structures Backup
'''
structure_dictionary = {
    1: (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                            0                              ',
    '                                       0    0                              ',
    '  11    111      111       1      011110111101110    1      11      111    '
    ),

    2: (
    '                                                                           ',
    '                                                                           ',
    '                                    10000                                  ',
    '                             000000000000                                  ',
    '               1      000    000000000000                                  ',
    '          0000000000000001111000000000000        111                       ',
    '     0000000000000000000000000000000000000000000000000000         111      '
    ),

    3:
    (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '            100000     11     110     11       111                         ',
    '     0000000000000000000000000000000000000000000000000      11     111     '
    ),

    4:
    (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '               0                                0                          ',
    '          0    0   0                       0    0   0                      ',
    '     011110111101110        111       011110111101110     11       111     '
    ),

    5:
    (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                     0                      0                              ',
    '                0    0   0             0    0   0                          ',
    '           011110111101110        011110111101110        01111011110       '
    ),

    6:
    (
    '                                                                           ',
    '                                                                           ',
    '                                      000                                  ',
    '                                 000                                       ',
    '                            000                      000                   ',
    '                       000                     000000000   000             ',
    '    111     111     0000001111111111111111111110000000001111111000011      '
    )
}
'''