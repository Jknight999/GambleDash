import pygame
import pygame.freetype
import math
import random

#pulls the player, spike, block, and button classes from the game_classes.py folder
from game_classes import Player, Spike, Block, Button

class GameScreenManager:
    #basic characteristics that the game screen manager uses
    def __init__(self, screen_to_draw, current_player, s_w, s_h, fl_color, f_r):
        self.surface = screen_to_draw
        self.screen_width = s_w
        self.screen_height = s_h
        self.f_c = fl_color
        self.framerate = f_r
        self.spikes = []
        self.blocks = []
        self.scroll_speed = 550
        self.clock = pygame.time.Clock()
        self.tick_counter = 0
        self.frame_counter = 0
        self.dt = 0
        self.previous_player_bottom = current_player.y + current_player.h

        #list of tuples of all possible structures for the level printer to use
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
    '                                     0000                                  ',
    '                             000000000000                                  ',
    '                   000000    000000000000                                  ',
    '            00000000000001111000000000000                                  ',
    '     0000000000000000000000000000000000000000000000000                     '
    ),
    3: (
    '00000000000000000000000000000000000000000                                  ',
    '00000000000000000000000000000000000000000                                  ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '       1        111              11                                        ',
    '000000000000000000000000000000000000000000000000000000                     '
    )
}
        self.current_structure = 2

        #returns a tuple with if the player is colliding with a block and the block it is colliding with
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

    def scroll(self):
        #scrolls each spike and places its hitbox (to handle collisions)
        for spike in self.spikes:
            spike.x -= self.scroll_speed * self.dt
            spike.hitbox.x = spike.x + spike.width / 2.5
        #scrolls each block and that block's mask (to handle collisions)
        for block in self.blocks:
            block.x -= self.scroll_speed * self.dt
            block.block.x = block.x
        #removes all blocks and spikes that go off of the screen
        self.discard_objects()

    def discard_objects(self):
        #makes a list of all spikes and blocks on the screen
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
            #if the value of the index in the list is a 1 then it adds a spike to the spike list
            if level[row_number][tick] == '1':
                self.spikes.append(Spike(screen.get_width(), (self.screen_height / 10) * row_number, SCREENWIDTH, SCREENHEIGHT))
            #if the value of the index in the list is a 0 then it adds a block to the block list
            elif level[row_number][tick] == '0':
                self.blocks.append(Block(screen.get_width(), (self.screen_height / 10) * row_number, SCREENWIDTH, SCREENHEIGHT))

    def tick(self, current_player):
        #calculates delta time from framerate
        self.dt = self.clock.tick(self.framerate) / 1000

        #scrolls the whole level
        self.scroll()

        #rotates the player if they're in the air
        if current_player.y < GROUND_Y - current_player.h and not self.player_block_colliding:
            current_player.rotate_player(self.dt)

        #checks for jumping every tick and applies gravity
        self.check_jump(current_player)
        self.previous_player_bottom = current_player.y + current_player.h
        GameScreenManager.apply_physics(current_player)

        #counts frames and converts them into ticks
        if self.frame_counter % math.floor(self.screen_width / 200) == 0:
            #reads through the structure list and prints out the correct structure
            if self.tick_counter < len(self.structures[self.current_structure][0]) - 1:
                self.tick_counter += 1
            else:
                self.tick_counter = 0
                #randomizes next structure
                self.current_structure = random.randint(1, len(self.structures))
            self.print_level(self.structures[self.current_structure], self.tick_counter)
        self.frame_counter += 1

        #converts the block collision tuple into two variables
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

        #checks spike and block collisions with the player
        for k in self.spikes:
            self.check_spike_player_collision(k, current_player)
        for k in self.blocks:
            player_died = self.check_block_player_collision(k, current_player)
            if player_died:
                break

        #keeps the player above the floor and the blocks
        self.check_ground_collisions(current_player)

        #draws the game screen and the objects contained in it at the moment
        self.draw_screen(self.f_c)
        self.draw_objects()

        #draws the player to the screen
        self.surface.blit(current_player.rotated_surface, current_player.rect)

    def check_jump(self, current_player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            #handles jumping when the player is on a block
            if self.player_block_colliding:
                current_player.y = self.colliding_with.y - current_player.h
                current_player.y_vel = current_player.jump_strength

            #jumping when player is on the ground
            if current_player.y >= GROUND_Y - current_player.h:
                current_player.y = GROUND_Y - current_player.h
                current_player.y_vel = current_player.jump_strength

    def draw_screen(self, floor_c):
        screen.blit(bg)
        #calculates so that the floor always draws 2/3 of the way down
        pygame.draw.rect(screen, floor_c, (0, GROUND_Y, self.screen_width, SCREENHEIGHT - GROUND_Y))
        #draws the back button to the screen
        back_button.draw_button(screen)
        back_button.render_text(self.surface)

    def check_ground_collisions(self, current_player):
        #checks if the player is on the ground
        if current_player.y >= GROUND_Y - current_player.h:
            current_player.y = GROUND_Y - current_player.h
            current_player.y_vel = 0

            #snaps the cube back to flat on the ground
            current_player.snap_rotation()

        #converts the block collision tuple into two variables
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)
        if self.player_block_colliding:
            current_player.y = self.colliding_with.y - current_player.h
            current_player.y_vel = 0

            #snaps the cube back to flat on the ground
            current_player.snap_rotation()

    def check_block_player_collision(self, blk, current_player):
        #find the players horizontal overlap with the block
        horizontal_overlap = current_player.rect.right > blk.block.left and current_player.rect.left < blk.block.right

        #find the players bottom and the top of the block
        player_bottom = current_player.y + current_player.h
        block_top = blk.block.y

        #check whether the players bottom crossed the blocks top during this frame while falling
        previous_bottom = self.previous_player_bottom

        landing = horizontal_overlap and current_player.y_vel > 0 and previous_bottom <= block_top <= player_bottom

        if landing:
            #place the player exactly on top of the block
            current_player.y = block_top - current_player.h
            current_player.y_vel = 0

            #reset rotation when landing
            current_player.snap_rotation()

            blk.colliding = True
        else:
            blk.colliding = False
            #only kill the player if they overlap the block
            offset_x = int(blk.block.x - current_player.rect.x)
            offset_y = int(blk.block.y - current_player.rect.y)

            if current_player.mask.overlap(blk.mask, (offset_x, offset_y)):
                self.reset_game(current_player)
                return True
        return False

    def check_spike_player_collision(self, spk, current_player):
        #finds offset amount from the spike hitbox to the player
        offset_x = int(spk.hitbox.x - current_player.rect.x)
        offset_y = int(spk.hitbox.y - current_player.rect.y)

        #if the player and mask overlap then reset the level
        if player.mask.overlap(spk.mask, (offset_x, offset_y)):
            screen.fill((0, 0, 0))
            self.reset_game(current_player)

    def draw_objects(self):
        for to_draw in self.spikes:
            #separates the output from the to_draw.find_vertices() function into 3 variables
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

    @staticmethod
    def apply_physics(current_player):
        #applies gravity and ground collision detection
        current_player.y_vel += current_player.gravity * game_screen.dt
        current_player.y += current_player.y_vel * game_screen.dt

    @staticmethod
    def is_block_colliding(all_blocks):
        #if the player is colliding with a block then return true and the block
        for block in all_blocks:
            if block.colliding:
                return True, block
        return False, None

def draw_menu_screen():
    screen.fill((17, 56, 171))
    play_button.draw_button(screen)
    play_button.render_text(screen)
    casino_button.draw_button(screen)
    casino_button.render_text(screen)

def draw_casino_screen():
    screen.fill((94, 6, 6))
    CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 4), f'Your Chips: {chips}', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20))
    back_button.draw_button(screen)
    back_button.render_text(screen)
    higher_or_lower_button.draw_button(screen)
    higher_or_lower_button.render_text(screen)

#text initialization and font storing
pygame.freetype.init()
gd_font_size = 80
gd_font = pygame.freetype.Font("Assets/pusab.otf", gd_font_size)
GD_FONTS = {
    14: pygame.freetype.Font('Assets/pusab.otf', 14),
    18: pygame.freetype.Font('Assets/pusab.otf', 18),
    24: pygame.freetype.Font('Assets/pusab.otf', 24),
    32: pygame.freetype.Font('Assets/pusab.otf', 32),
    50: pygame.freetype.Font('Assets/pusab.otf', 50),
    100: pygame.freetype.Font('Assets/pusab.otf', 100)
}
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

#screen setup
FRAMERATE = 120
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * 0.5
SHOW_SPIKE_HITBOXES = False
GROUND_Y = math.floor(0.7 * SCREENHEIGHT)
floor_color = [9, 30, 92]
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync = 1)
bg = pygame.image.load("assets/background.jpg").convert()

#initializes first instances of class
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

#game buttons
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), ('X', "Assets/pusab.otf", SCREENHEIGHT / 20, (245, 200, 76)))
higher_or_lower_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), ('Higher or Lower', 'Assets/casino.ttf', 40, (0, 0, 0)))

#screen and basic variable initialization
game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, FRAMERATE)
pygame.display.set_caption("GambleDash")
chips= 100

#boolean initialization
running = True
in_menu = True
in_game = False
in_casino = False

while running:
    #event handling
    for event in pygame.event.get():
        #quit event handle
        if event.type == pygame.QUIT:
            running = False

        #button click event handling
        if play_button.check_button_click(event):
            if in_menu:
                in_game = True
                in_menu = False
                GameScreenManager.reset_game(game_screen, player)
        if casino_button.check_button_click(event):
            if in_menu:
                in_casino = True
                in_menu = False
        if back_button.check_button_click(event):
            if not in_menu:
                in_menu = True
                in_casino = False
                in_game = False

    if in_game:
        game_screen.tick(player)
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()

    pygame.display.flip()