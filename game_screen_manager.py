import pygame
import random
import math
from game_classes import Spike, Block

class GameScreenManager:
    #basic characteristics that the game screen manager uses
    def __init__(self, screen_to_draw, current_player, s_w, s_h, fl_color, f_r, ground_y, show_spike_hitboxes, bg, back_button):
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
        self.g_y = ground_y
        self.spike_hitboxes = show_spike_hitboxes
        self.bg = bg
        self.previous_player_bottom = current_player.y + current_player.h
        self.back_button = back_button

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
        self.current_structure = random.randint(1, len(self.structures))

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
                self.spikes.append(Spike(self.surface.get_width(), (self.screen_height / 10) * row_number, self.screen_width, self.screen_height))
            #if the value of the index in the list is a 0 then it adds a block to the block list
            elif level[row_number][tick] == '0':
                self.blocks.append(Block(self.surface.get_width(), (self.screen_height / 10) * row_number, self.screen_width, self.screen_height))

    def tick(self, current_player):
        #calculates delta time from framerate
        self.dt = self.clock.tick(self.framerate) / 1000

        #scrolls the whole level
        self.scroll()

        #rotates the player if they're in the air
        if current_player.y < self.g_y - current_player.h and not self.player_block_colliding:
            current_player.rotate_player(self.dt)

        #checks for jumping every tick and applies gravity
        self.check_jump(current_player)
        self.previous_player_bottom = current_player.y + current_player.h
        GameScreenManager.apply_physics(self, current_player)

        #counts frames and converts them into ticks
        if self.frame_counter % math.floor(self.screen_width / 200) == 0:
            #reads through the structure list and prints out the correct structure
            if self.tick_counter < len(self.structures[self.current_structure][0]) - 1:
                self.tick_counter += 1
            else:
                self.tick_counter = 0
                #randomizes next structure
                temp = self.current_structure
                while temp == self.current_structure:
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
            if current_player.y >= self.g_y - current_player.h:
                current_player.y = self.g_y - current_player.h
                current_player.y_vel = current_player.jump_strength

    def draw_screen(self, floor_c):
        self.surface.blit(self.bg)
        #calculates so that the floor always draws 2/3 of the way down
        pygame.draw.rect(self.surface, floor_c, (0, self.g_y, self.screen_width, self.screen_height - self.g_y))
        #draws the back button to the screen
        self.draw_objects()
        self.back_button.draw_button(self.surface)
        self.back_button.render_text(self.surface)

    def check_ground_collisions(self, current_player):
        #checks if the player is on the ground
        if current_player.y >= self.g_y - current_player.h:
            current_player.y = self.g_y - current_player.h
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
        if current_player.mask.overlap(spk.mask, (offset_x, offset_y)):
            self.surface.fill((0, 0, 0))
            self.reset_game(current_player)

    def draw_objects(self):
        for to_draw in self.spikes:
            #separates the output from the to_draw.find_vertices() function into 3 variables
            v_a, v_b, v_c = to_draw.find_vertices()
            pygame.draw.polygon(self.surface, (0, 0, 0), (v_a, v_b, v_c))

            #shrinking the vertices inwards so that the outline doesn't go outside the block allotted
            v_a[0] += 5
            v_a[1] -= 3
            v_b[1] += 3
            v_c[0] -= 5
            v_c[1] -= 3
            pygame.draw.polygon(self.surface, (255, 255, 255), (v_a, v_b, v_c), width=3)
            if self.spike_hitboxes:
                pygame.draw.rect(self.surface, (255, 0, 0), to_draw.hitbox, width=1)

        #draws blocks to the screen
        for to_draw in self.blocks:
            self.surface.blit(to_draw.image, to_draw.block)

    #resets the game
    def reset_game(self, current_player):
        current_player.__init__(self.screen_width, self.screen_height, self.g_y)
        self.spikes = []
        self.blocks = []
        self.tick_counter = 0
        self.frame_counter = 0

    def apply_physics(self, current_player):
        #applies gravity and ground collision detection
        current_player.y_vel += current_player.gravity * self.dt
        current_player.y += current_player.y_vel * self.dt

    @staticmethod
    def is_block_colliding(all_blocks):
        #if the player is colliding with a block then return true and the block
        for block in all_blocks:
            if block.colliding:
                return True, block
        return False, None