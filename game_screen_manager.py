from game_classes import Player, Spike, Block, Button
import math
import pygame

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
    '                                     0000                                  ',
    '                             000000000000                                  ',
    '                   000000    000000000000                                  ',
    '            00000000000001111000000000000                                  ',
    '     0000000000000000000000000000000000000000000000000                     '
    ),

    3: (
        '                                                                           ',
        '                                                                           ',
        '                                                                           ',
        '                                                                           ',
        '                                                                           ',
        '             00000                                                         ',
        '     0000000000000000000000000000000000000000000000000                     '
    )
}
        self.current_structure = 2
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
        for spike in self.spikes:
            if spike.x + spike.width < 0:
                self.spikes.remove(spike)
        for block in self.blocks:
            if block.x + block.width < 0:
                self.blocks.remove(block)

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
            # checks for each block if they are colliding with the player using colliderect
            if current_player.rect.colliderect(k.block) and current_player.x < k.x + k.width:
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
        # checks if the y velocity is less than or equal to 0 or its way below the block
        offset_x = int(blk.block.x - current_player.rect.x)
        offset_y = int(blk.block.y - current_player.rect.y)

        if (current_player_yv <= 0 or current_player.y >= blk.y) and current_player.mask.overlap(blk.mask, (offset_x, offset_y)):
            self.surface.fill((0, 0, 0))
            self.reset_game(current_player)
            return
        if current_player_yv > 0:
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