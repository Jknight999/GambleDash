import pygame
import pygame.freetype
import math
import random
import game_classes as gc
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
player = gc.Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

# I have absolutely no idea why but this is necessary to make the cube start the right way up
player.angle = 91
player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
player.rect = player.rotated_surface.get_rect(center=(player.x + player.w // 2, player.y + player.h // 2))

#now takes a text argument - ('text', 'font file name', size, color(R,G,B))
play_button = gc.Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = gc.Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))
back_button = gc.Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), ('X', "Assets/pusab.otf", SCREENHEIGHT / 20, (245, 200, 76)))
higher_or_lower_button = gc.Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), ('Higher or Lower', 'Assets/casino.ttf', 40, (0, 0, 0)))

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
        higher_or_lower_button.check_button_click(event)

    if in_game:
        draw_game_screen()
        game_screen.tick(player)
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()

    pygame.display.flip()