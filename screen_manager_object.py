import pygame
import pygame.freetype
import math

#to push

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
        self.image = pygame.image.load("Assets/playerskin02.png").convert_alpha()
        #sets the size to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        # draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        # creates mask for collision handling
        self.mask = pygame.mask.from_surface(self.rotated_surface)

    def rotate_player(self):
        self.angle = (self.angle + self.rotation_speed * game_screen.dt) % 360
        # rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        # updates collision mask
        self.mask = pygame.mask.from_surface(self.rotated_surface)


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

        self.surface = pygame.Surface((self.block.width, self.block.height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0))

        self.mask = pygame.mask.from_surface(self.surface)

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
        global in_menu
        global in_game
        global in_casino
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
    def __init__(self, screen_to_draw, current_player):
        self.surface = screen_to_draw
        self.player = current_player
        self.spikes = []
        self.blocks = []
        self.buttons = []
        self.scroll_speed = 550
        self.clock = pygame.time.Clock()
        self.tick_counter = 0
        self.frame_counter = 0
        self.dt = 0
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
    '                                                                           ',
    '                                                                           ',
    '                                                                           ',
    '                                                                           '
    )
}
        self.current_structure = 1
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

    def scroll(self):
        for spike in self.spikes:
            spike.x -= self.scroll_speed * self.dt
            spike.hitbox.x = spike.x + spike.width / 2.5
        for block in self.blocks:
            block.x -= self.scroll_speed * self.dt
            block.block.x = block.x

    def print_level(self, level, tick):
        for row_number in range(len(level)):
            if level[row_number][tick] == '1':
                self.spikes.append(Spike(screen.get_width(), (SCREENHEIGHT / 10) * row_number))
            elif level[row_number][tick] == '0':
                self.blocks.append(Block(screen.get_width(), (SCREENHEIGHT / 10) * row_number))

    def tick(self, current_player):
        #converts the tuple into two variables to work with throughout the code
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)

        #scrolls the whole level
        self.scroll()

        # counts frames and converts into ticks
        if self.frame_counter % math.floor(SCREENWIDTH / 200) == 0:
            if self.tick_counter < len(self.structures[self.current_structure][0]) - 1:
                self.tick_counter += 1
            else:
                self.tick_counter = 0
            self.print_level(self.structures[self.current_structure], self.tick_counter)
        self.frame_counter += 1

        # calculates delta time from framerate
        self.dt = self.clock.tick(FRAMERATE) / 1000

        #draws the game screen and the objects contained
        GameScreenManager.draw_screen(floor_color)
        self.draw_objects()

        # checks the collisions - rn the spike collision check is outside the class and the block is within
        # fix it if you have time
        for k in self.spikes:
            self.check_spike_player_collision(k)
        for k in self.blocks:
            self.check_block_player_collision(k)

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
    @staticmethod
    def draw_screen(floor_c):
        screen.blit(bg)
        # calculates so that the floor always draws 2/3 of the way down
        pygame.draw.rect(screen, floor_c, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))
        back_button.draw_button(screen)
        back_button.render_text()

    @staticmethod
    def apply_physics(current_player):
        # applies gravity and ground collision detection
        current_player.y_vel += current_player.gravity * game_screen.dt
        current_player.y += current_player.y_vel * game_screen.dt

    @staticmethod
    def is_block_colliding(all_blocks):
        for b in all_blocks:
            if b.colliding:
                return True, b
        return False, None

    def check_ground_collisions(self, current_player):
        if current_player.y >= GROUND_Y - current_player.h:
            current_player.y = GROUND_Y - current_player.h
            current_player.y_vel = 0
            # snaps the cube back to flat on the ground
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)
        current_player.rect = current_player.rotated_surface.get_rect(center=(current_player.x + current_player.w // 2, current_player.y + current_player.h // 2))
        # updates mask again
        current_player.mask = pygame.mask.from_surface(current_player.rotated_surface)
        self.player_block_colliding, self.colliding_with = GameScreenManager.is_block_colliding(self.blocks)
        if self.player_block_colliding:
            current_player.y = self.colliding_with.y - current_player.h
            current_player.y_vel = 0
            # snaps the cube back to flat on the ground
            current_player.angle = round(current_player.angle / 90) * 90 % 360
            current_player.rotated_surface = pygame.transform.rotate(current_player.image, current_player.angle)

    def check_block_player_collision(self, block):
        # finds offset amount from the hitbox to the player
        offset_x = int(block.block.x - player.rect.x)
        offset_y = int(block.block.y - player.rect.y)

        if player.mask.overlap(player.mask, (offset_x, offset_y)) and player.y > block.block.y + SCREENHEIGHT/ 100 - player.h:
            screen.fill((255, 0, 0))
            self.reset_game(player)
        # if the player and mask overlap then reset the level
        if block.block.x - player.rect.w <= player.rect.x <= block.block.x + block.width and block.block.y - SCREENHEIGHT / 200 <= player.rect.y + player.rect.h <= block.block.y + SCREENHEIGHT / 100:
            block.colliding = True
            player.rect.y = block.block.y - player.rect.h
            player.y_vel = 0
            player.angle = round(player.angle / 90) * 90 % 360
            player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
        else:
            block.colliding = False

    def check_spike_player_collision(self, spike):

        # finds offset amount from the hitbox to the player
        offset_x = int(spike.hitbox.x - player.rect.x)
        offset_y = int(spike.hitbox.y - player.rect.y)

        # if the player and mask overlap then reset the level
        if player.mask.overlap(spike.mask, (offset_x, offset_y)):
            screen.fill((255, 0, 0))
            self.reset_game(player)

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
        for to_draw in self.blocks:
            pygame.draw.rect(screen, (9, 30, 92), to_draw.block)


    def reset_game(self, current_player):
        current_player.__init__(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)
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

# lists of generated instances of the classes to allow for multiple to be on screen

game_screen = GameScreenManager(screen, player)
pygame.display.set_caption("GambleDash")
chips= 100
dt = 0
running = True
in_menu = True
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
        back_button.check_button_click(event, "Back")

    if in_game:
        game_screen.tick(player)
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()

    #4. Update and Wait
    pygame.display.flip()