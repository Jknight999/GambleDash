import pygame
import pygame.freetype
import math
import random

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
        self.image = pygame.image.load("Assets/playerskin0" + str(random.randint(1,6)) + ".png").convert_alpha()
        #sets the size to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        # draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        # creates mask for collision handling
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_player(self):
        #calculates and sets rotation angle
        self.angle = (self.angle + self.rotation_speed * game_screen.dt) % 360
        # rotates the surface
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

        # makes the hitbox into a surface
        self.surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0))

        # draws a mask around the surface
        self.mask = pygame.mask.from_surface(self.surface)

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        #needed because triangles drawn through draw.polygon()
        # These vertices should not be used for hitboxes, spike hitboxes are rectangular
        return [[self.x, self.y + self.height], [self.x + self.width / 2, self.y], [self.x + self.width, self.y + self.height]]

class Block:
    # spike characteristics
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SCREENWIDTH / 20
        self.height = SCREENHEIGHT / 10
        self.speed = 550
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

        #makes the block a sprite
        self.image = pygame.image.load("Assets/gambledashblock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        #draws a mask around the image for collisions
        self.mask = pygame.mask.from_surface(self.image)

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

    #checks if the button is clicked
    def check_button_click(self, click_event, button_type):
        global in_menu, in_game, in_casino
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1:
                if button_type == "Play":
                    if in_menu:
                        in_game = True
                        in_menu = False
                    else:
                        pass
                elif button_type == "Gamble":
                    if in_menu:
                        in_casino = True
                        in_menu = False
                    else:
                        pass
                elif button_type == "Back":
                    if not in_menu:
                        in_menu = True
                        in_casino = False
                        in_game = False

class GameScreenManager:
    #basic characteristics
    def __init__(self, screen_to_draw, current_player, s_w, s_h, fl_color, f_r):
        self.surface = screen_to_draw
        self.screen_width = s_w
        self.screen_height = s_h
        self.f_c = fl_color
        self.framerate = f_r
        self.player = current_player
        self.spikes = []
        self.blocks = []
        self.buttons = []
        self.scroll_speed = 550
        self.clock = pygame.time.Clock()
        self.tick_counter = 0
        self.frame_counter = 0
        self.dt = 0
        #all possible structures
        self.structures = {
    1: (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                            0                              ',
    '                                       0    0                              ',
    '        111        1       1      01111011110111            11       1     '
    ),

    2: (
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                   11                                      ',
    '                   000000    000000000000                                  ',
    '            000000000000011110000000000000000000                           ',
    '     0000000000000000000000000000000000000000000000                        '
    )
}
        self.current_structure = 2
        #returns tuple of if the player is colliding with a block
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

    def scroll(self):
        #scrolls spike and places hitbox
        for spike in self.spikes:
            spike.x -= self.scroll_speed * self.dt
            spike.hitbox.x = spike.x + spike.width / 2.5
        #scrolls block and block mask
        for block in self.blocks:
            block.x -= self.scroll_speed * self.dt
            block.block.x = block.x

    def print_level(self, level, tick):
        #goes through each item in the structures list
        for row_number in range(len(level)):
            #if it is a 1 then makes a spike
            if level[row_number][tick] == '1':
                self.spikes.append(Spike(screen.get_width(), (self.screen_height / 10) * row_number))
            #if it is a 0 then makes a block
            elif level[row_number][tick] == '0':
                self.blocks.append(Block(screen.get_width(), (self.screen_height / 10) * row_number))

    def tick(self, current_player):
        # calculates delta time from framerate
        self.dt = self.clock.tick(self.framerate) / 1000

        #converts the tuple into two variables to work with throughout the code
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

        #scrolls the whole level
        self.scroll()

        # counts frames and converts into ticks
        if self.frame_counter % math.floor(self.screen_width / 200) == 0:
            if self.tick_counter < len(self.structures[self.current_structure][0]) - 1:
                self.tick_counter += 1
            else:
                self.tick_counter = 0
            self.print_level(self.structures[self.current_structure], self.tick_counter)
        self.frame_counter += 1

        #draws the game screen and the objects contained
        self.draw_screen(self.f_c)
        self.draw_objects()

        # checks spike and block collisions
        for k in self.spikes:
            self.check_spike_player_collision(k, current_player)
        for k in self.blocks:
            self.check_block_player_collision(k, current_player)

        # checks for jumping every tick and applies gravity
        self.check_jump(current_player)
        GameScreenManager.apply_physics(current_player)

        # keeps the player above the floor and the blocks
        self.check_ground_collisions(current_player)

        # rotates the player if they're in the air
        if current_player.y < GROUND_Y - current_player.h and not self.player_block_colliding:
            current_player.rotate_player()

        # draws the player to the screen
        self.surface.blit(current_player.rotated_surface, current_player.rect)

    def check_jump(self, current_player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            # touching a block
            if self.player_block_colliding:
                current_player.y = self.colliding_with.y - current_player.h
                current_player.y_vel = current_player.jump_strength

            # touching the ground
            if current_player.y >= GROUND_Y - current_player.h:
                current_player.y = GROUND_Y - current_player.h
                current_player.y_vel = current_player.jump_strength

    # these can be static methods since they do not edit any objects within this class, but should still be here for organization
    def draw_screen(self, floor_c):
        screen.blit(bg)
        # calculates so that the floor always draws 2/3 of the way down
        pygame.draw.rect(screen, floor_c, (0, GROUND_Y, self.screen_width, SCREENHEIGHT - GROUND_Y))
        #draws the back button to the screen
        back_button.draw_button(screen)
        back_button.render_text()

    @staticmethod
    def apply_physics(current_player):
        # applies gravity and ground collision detection
        current_player.y_vel += current_player.gravity * game_screen.dt
        current_player.y += current_player.y_vel * game_screen.dt

    @staticmethod
    def is_block_colliding(all_blocks):
        #if the player is colliding with a block then return true and the block
        for b in all_blocks:
            if b.colliding:
                return True, b
        return False, None

    def check_ground_collisions(self, current_player):
        #checks if the player is on the ground
        if current_player.y >= GROUND_Y - current_player.h:
            current_player.y = GROUND_Y - current_player.h
            current_player.y_vel = 0

            # snaps the cube back to flat on the ground
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)
        current_player.rect = current_player.rotated_surface.get_rect(center=(current_player.x + current_player.w // 2, current_player.y + current_player.h // 2))

        # updates mask again
        current_player.mask = pygame.mask.from_surface(current_player.image)
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)
        if self.player_block_colliding:
            current_player.y = self.colliding_with.y - current_player.h
            current_player.y_vel = 0

            # snaps the cube back to flat on the ground
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)

    def check_block_player_collision(self, blk, current_player):
        # finds offset amount from the hitbox to the player
        offset_x = int(blk.block.x - current_player.rect.x)
        offset_y = int(blk.block.y - current_player.rect.y)

        #if the player hits the side of the block then reset the game
        if current_player.mask.overlap(current_player.mask, (offset_x, offset_y)) and current_player.y > blk.block.y + SCREENHEIGHT/ 100 - current_player.h:
            screen.fill((0, 0, 0))
            self.reset_game(current_player)

        # if the player and mask overlap then reset the level
        if blk.block.x - current_player.rect.w <= current_player.rect.x <= blk.block.x + blk.width and blk.block.y - SCREENHEIGHT / 200 <= current_player.rect.y + current_player.rect.h <= blk.block.y + SCREENHEIGHT / 100:
            blk.colliding = True
            current_player.rect.y = blk.block.y - player.rect.h
            current_player.y_vel = 0
            current_player.angle = round(player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
        else:
            blk.colliding = False

    def check_spike_player_collision(self, spk, current_player):
        # finds offset amount from the hitbox to the player
        offset_x = int(spk.hitbox.x - current_player.rect.x)
        offset_y = int(spk.hitbox.y - current_player.rect.y)

        # if the player and mask overlap then reset the level
        if player.mask.overlap(spk.mask, (offset_x, offset_y)):
            screen.fill((0, 0, 0))
            self.reset_game(current_player)

    def draw_objects(self):
        for to_draw in self.spikes:
            # giving myself the ability to separate the vertices
            v_a, v_b, v_c = to_draw.find_vertices()
            pygame.draw.polygon(screen, (0, 0, 0), (v_a, v_b, v_c))

            # shrinking the vertices inwards so that the outline doesn't go outside the block allotted
            v_a[0] += 5
            v_a[1] -= 3
            v_b[1] += 3
            v_c[0] -= 5
            v_c[1] -= 3
            pygame.draw.polygon(screen, (255, 255, 255), (v_a, v_b, v_c), width=3)
            if SHOW_SPIKE_HITBOXES:
                pygame.draw.rect(screen, (255, 0, 0), to_draw.hitbox, width=1)

        #draws blocks to the screen
        for to_draw in self.blocks:
            screen.blit(to_draw.image, to_draw.block)

    #resets the game
    def reset_game(self, current_player):
        current_player.__init__(self.screen_width, SCREENHEIGHT, GROUND_Y)
        self.spikes = []
        self.blocks = []
        self.tick_counter = 0
        self.frame_counter = 0

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
    back_button.draw_button(screen)
    back_button.render_text()
    higher_or_lower_button.draw_button(screen)
    higher_or_lower_button.render_text()

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

# New level data list
# 1 is a spike, 0 is a block, ' ' is nothing

bg = pygame.image.load("assets/background.jpg").convert()

#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

#now takes a text argument - ('text', 'font file name', size, color(R,G,B))
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), ('X', "Assets/pusab.otf", SCREENHEIGHT / 20, (245, 200, 76)))
higher_or_lower_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), ('Higher or Lower', 'Assets/casino.ttf', 40, (0, 0, 0)))

# lists of generated instances of the classes to allow for multiple to be on screen

game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, FRAMERATE)
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
        play_button.check_button_click(event, "Play")
        casino_button.check_button_click(event, "Gamble")
        back_button.check_button_click(event, "Back")
        higher_or_lower_button.check_button_click(event, "Higher or Lower")

    if in_game:
        game_screen.tick(player)
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()

    pygame.display.flip()