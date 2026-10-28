import pygame
import pygame.freetype
import math

from game_classes import Player, Button
from game_screen_manager import GameScreenManager
from blackjack import CasinoScreenManager
from rabbi_yosef_voice_lines import voice_lines

pygame.init()
pygame.mixer.init()
pygame.freetype.init()

def draw_menu_screen():
    draw_game_screen()
    font = GD_FONTS[50]
    chip_text = str(chips)
    text_rect = font.get_rect(chip_text)
    text_rect.right = SCREENWIDTH - 70
    font.render_to(screen, text_rect, chip_text, (255, 255, 255))

    chips_icon = pygame.image.load("Assets/chipsicon.png").convert_alpha()
    screen.blit(chips_icon, (SCREENWIDTH - 60, 30))

    play_button.draw_button(screen)
    play_button.render_text(screen)
    casino_button.draw_button(screen)
    casino_button.render_text(screen)

def draw_casino_screen():
    screen.fill((94, 6, 6))
    CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20))
    back_button.draw_button(screen)
    back_button.render_text(screen)
    blackjack_button.draw_button(screen)
    blackjack_button.render_text(screen)

def draw_game_screen():
    screen.blit(bg)
    # calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor_color, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))
    #draws the back button to the screen
    if game_screen.player_alive and not in_menu:
        back_button.draw_button(screen)
        back_button.render_text(screen)
        font = GD_FONTS[50]
        text = "+" + str(game_screen.run_chips)
        text_rect = font.get_rect(text)
        text_rect.right = SCREENWIDTH - 30
        font.render_to(screen, text_rect, text, (255, 255, 255))

def draw_death_screen():
    if not game_screen.player_alive:
        font = GD_FONTS[50]
        chip_text = str(chips)
        text_rect = font.get_rect(chip_text)
        text_rect.right = SCREENWIDTH - 70
        font.render_to(screen, text_rect, chip_text, (255, 255, 255))
        run_text = "+" + str(game_screen.run_chips)
        run_text_rect = font.get_rect(run_text)
        run_text_rect.right = SCREENWIDTH - 70
        run_text_rect.top = 80
        font.render_to(screen, run_text_rect, run_text, (255, 255, 255))
        chips_icon = pygame.image.load("Assets/chipsicon.png").convert_alpha()
        screen.blit(chips_icon, (SCREENWIDTH - 60, 30))
        back_button.draw_button(screen)
        back_button.render_text(screen)
        continue_button.draw_button(screen)
        continue_button.render_text(screen)
        casino_button.draw_button(screen)
        casino_button.render_text(screen)

def draw_loan_screen():
    screen.fill((135, 206, 250))
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('Assets/completely_innocent_song.mp3')
        pygame.mixer.music.play(-1)
    pygame.draw.rect(screen, (126, 200, 80), (0, 2 * SCREENHEIGHT / 3, SCREENWIDTH, SCREENHEIGHT / 2.9))
    bank = pygame.image.load("Assets/bank.png").convert_alpha()
    bank = pygame.transform.scale(bank, (3 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 5))
    rabbi_yosef = pygame.image.load("Assets/rabbiyosef.png").convert_alpha()
    rabbi_yosef = pygame.transform.scale(rabbi_yosef, (4 * SCREENWIDTH / 10, 4 * SCREENHEIGHT / 5))
    screen.blit(bank, (SCREENWIDTH / 10, SCREENHEIGHT / 5))
    screen.blit(rabbi_yosef, (SCREENWIDTH - 350, SCREENHEIGHT - 300))
    voice_line_text = current_voice_line
    voice_line_text_rect = GD_FONTS[18].get_rect(voice_line_text)
    voice_line_text_rect.x = 300
    voice_line_text_rect.y = 300
    lines = current_voice_line.split("\n")

    y = 100
    for line in lines:
        voice_line_text_rect = GD_FONTS[32].get_rect(line)
        voice_line_text_rect.x = 450
        voice_line_text_rect.y = y
        GD_FONTS[32].render_to(screen, voice_line_text_rect, line, (255, 255, 255))
        y += 30

def blur_screen():
    screen_copy = screen.copy()
    #apparently making the screen smaller is more efficient for blurring
    small_screen = (SCREENWIDTH // 4, SCREENHEIGHT // 4)
    small_surface = pygame.transform.scale(screen_copy, small_screen)
    pygame.transform.box_blur(small_surface, radius=3)
    blurred_screen = pygame.transform.smoothscale(small_surface, (SCREENWIDTH, SCREENHEIGHT))
    screen.blit(blurred_screen)

#screen setup
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * 0.5
#where the top of the floor is (for collision physics principles)
GROUND_Y = math.floor(0.7 * SCREENHEIGHT)
SHOW_SPIKE_HITBOXES = True

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

# initializes the font with default size
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

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync= 1)
bg = pygame.image.load("assets/background.png").convert()
bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))

#initializes first instances of class
player= Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

# I have absolutely no idea why but this is necessary to make the cube start the right way up
player.angle = 91
player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
player.rect = player.rotated_surface.get_rect(center=(player.x + player.w // 2, player.y + player.h // 2))

#now takes a text argument - ('text', 'font file name', size, color(R,G,B))
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), ('Dash', "Assets/pusab.otf", 100, (255, 255, 255)))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 4, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), ('Gamble', 'Assets/casino.ttf', 80, (0, 0, 0)))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), ('X', "Assets/pusab.otf", SCREENHEIGHT / 20, (245, 200, 76)))
blackjack_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), ('Blackjack', 'Assets/casino.ttf', 40, (0, 0, 0)))
continue_button = Button(SCREENWIDTH / 4, SCREENHEIGHT / 4, SCREENWIDTH / 2, SCREENHEIGHT / 5, (14, 237, 70), ('Continue for 50 Chips?', 'Assets/pusab.otf', 40, (0, 0, 0)))

#in a list, so IT CAN CHANGE
floor_color = [0,42,124]
chips = 100
voice_line_num = 1
current_voice_line = voice_lines[voice_line_num]
game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, GROUND_Y, bg)
casino_screen = CasinoScreenManager(screen, chips, SCREENWIDTH, SCREENHEIGHT)

pygame.display.set_caption("GambleDash")
running = True
in_menu = True
in_game = False
in_casino = False
in_death_screen = False
in_loan_screen = False

while running:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_loan_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    voice_line_num += 1
                    if voice_line_num >= 8:
                        voice_line_num = 8
                    current_voice_line = voice_lines[voice_line_num]

        # sends event to button to see if it's been clicked
        if in_menu:
            if play_button.check_button_click(event):
                if chips >= 50:
                    in_menu = False
                    in_game = True
                    chips -= 50
                    game_screen.run_chips = 0
                    game_screen.reset_game(game_screen.player)
                else:
                    in_loan_screen = True
                    in_menu = False
                    draw_loan_screen()
            if casino_button.check_button_click(event):
                in_menu = False
                in_casino = True
        if in_death_screen:
            if casino_button.check_button_click(event):
                in_casino = True
                in_death_screen = False
                chips += game_screen.run_chips
        if in_casino:
            if blackjack_button.check_button_click(event):
                chips = casino_screen.play_blackjack()
            if back_button.check_button_click(event):
                in_casino = False
                in_menu = True
        if in_death_screen:
            if back_button.check_button_click(event):
                in_death_screen = False
                in_menu = True
                chips += game_screen.run_chips
        if in_game:
            if back_button.check_button_click(event):
                in_game = False
                in_menu = True
        if in_death_screen:
            if continue_button.check_button_click(event):
                if chips >= 50:
                    chips -= 50
                    in_death_screen = False
                    in_game = True
                    game_screen.reset_game(game_screen.player)
                else:
                    in_menu = False
                    in_death_screen = False
                    in_loan_screen = True
                    voice_line_num = 1

    if in_game:
        draw_game_screen()
        game_screen.tick(player)
        if not game_screen.player_alive:
            draw_game_screen()
            blur_screen()
            in_game = False
            in_death_screen = True
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()
    elif in_death_screen:
        draw_death_screen()
    elif in_loan_screen:
        draw_loan_screen()

    pygame.display.flip()