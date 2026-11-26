#imports
import pygame
import pygame.freetype
import math
import fonts
import random

from game_classes import Player, Button
from game_screen_manager import GameScreenManager
from casino_screen_manager import CasinoScreenManager
from loan_shark_voice_lines import voice_lines
import structures

#inits
pygame.init()
pygame.mixer.init()
pygame.freetype.init()

def place_chips_on_screen():
    # takes the players chips and renders it to the screen
    chip_text = str(chips)
    text_rect = fonts.GD_FONTS[50].get_rect(chip_text)
    text_rect.right = SCREENWIDTH * 0.95 - 40
    text_rect.bottom = 85

    # makes a rectangle and places it based off of the text rect
    border_rect = pygame.Rect(100, 100, 100, 100)
    border_rect.width = text_rect.width + 60
    border_rect.right = SCREENWIDTH * 0.95
    border_rect.height = 30 + text_rect.height
    border_rect.bottom = text_rect.bottom + 15

    # draws it and adds a border
    pygame.draw.rect(screen, (0, 0, 0), border_rect, border_radius=20)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, width=2, border_radius=20)

    fonts.GD_FONTS[50].render_to(screen, text_rect, chip_text, (255, 255, 255))
    screen.blit(chips_icon, (SCREENWIDTH * 0.95 - 30, 30))

def draw_screen_bg():
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, floor_color, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))

    scan_x = 0
    scan_y = 0
    level = structures.home_screen_structures[1]
    for row in level:
        for item in row:
            if item == '0':
                screen.blit(block, (scan_x, scan_y))
            if item == 'u':
                v1 = scan_x + 3, scan_y
                v2 = scan_x + SCREENWIDTH / 20 - 5, scan_y
                v3 = (v1[0] + v2[0]) / 2, scan_y + SCREENHEIGHT / 10
                pygame.draw.polygon(screen, (0, 0, 0), [v1, v2, v3])
                pygame.draw.polygon(screen, (255, 255, 255), [v1, v2, v3], width=3)
            if item == '1':
                v1 = scan_x + 3, scan_y + SCREENHEIGHT / 10
                v2 = scan_x + SCREENWIDTH / 20 - 5, scan_y + SCREENHEIGHT / 10
                v3 = (v1[0] + v2[0]) / 2, scan_y
                pygame.draw.polygon(screen, (0, 0, 0), [v1, v2, v3])
                pygame.draw.polygon(screen, (255, 255, 255), [v1, v2, v3], width=3)
            scan_x += SCREENWIDTH / 20
        scan_y += SCREENHEIGHT / 10
        scan_x = 0

def draw_menu_screen():
    draw_screen_bg()

    place_chips_on_screen()

    #draws play and casino buttons
    play_button.draw_button(screen)
    screen.blit(play_icon, (SCREENWIDTH * 0.4475, SCREENHEIGHT * 0.285))
    casino_button.draw_button(screen)
    screen.blit(casino_icon, (SCREENWIDTH * 0.6875, SCREENHEIGHT * 0.3125))
    shop_button.draw_button(screen)
    screen.blit(shop_icon, (SCREENWIDTH * 0.2225, SCREENHEIGHT * 0.3125))

def draw_casino_screen():
    #handles screen background and text
    screen.fill((94, 6, 6))
    fonts.CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20), border_radius=20)
    place_chips_on_screen()

    screen.blit(casino_shark, (6.5 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 10))
    #draws back, blackjack, and poker buttons
    back_button.draw_button(screen)
    blackjack_button.draw_button(screen)
    poker_button.draw_button(screen)

def draw_game_screen():
    screen.blit(bg)

    #calculates so that the floor always draws 2/3 of the way down
    pygame.draw.rect(screen, floor_color, (0, GROUND_Y, SCREENWIDTH, SCREENHEIGHT - GROUND_Y))
    
    #draws the back button to the screen
    if game_screen.player_alive and not in_menu:
        back_button.draw_button(screen)
        text = "+" + str(game_screen.run_chips)
        text_rect = fonts.GD_FONTS[50].get_rect(text)
        text_rect.right = SCREENWIDTH - 30
        fonts.GD_FONTS[50].render_to(screen, text_rect, text, (255, 255, 255))

def draw_death_screen():
    if not game_screen.player_alive:
        draw_screen_bg()
        #resets run chips and renders chips to the screen
        game_screen.run_chips = 0

        place_chips_on_screen()
        
        #draws back, continue, and casino buttons
        back_button.draw_button(screen)
        continue_button.draw_button(screen)
        screen.blit(play_icon, (SCREENWIDTH * 0.4475, SCREENHEIGHT * 0.285))
        casino_button.draw_button(screen)
        screen.blit(casino_icon, (SCREENWIDTH * 0.6875, SCREENHEIGHT * 0.3125))
        shop_button.draw_button(screen)
        screen.blit(shop_icon, (SCREENWIDTH * 0.2225, SCREENHEIGHT * 0.3125))

def draw_loan_screen():
        
    if voice_line_num != 5:
        #handles background, text, and sprites
        screen.fill((135, 206, 250))
        pygame.draw.rect(screen, (126, 200, 80), (0, 2 * SCREENHEIGHT / 3, SCREENWIDTH, SCREENHEIGHT / 2.9))
        screen.blit(bank, (SCREENWIDTH / 10, SCREENHEIGHT / 5))
        screen.blit(loan_shark, (6.5 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 10))
        voice_line_text = current_voice_line
        voice_line_text_rect = fonts.GD_FONTS[18].get_rect(voice_line_text)
        voice_line_text_rect.x =  0
        voice_line_text_rect.y = SCREENHEIGHT / 5
        
        #places the voice lines so that they are written in lines to the screen
        lines = current_voice_line.split("\n")
        y = voice_line_text_rect.y
        for line in lines:
            voice_line_text_rect = fonts.GD_FONTS[32].get_rect(line)
            voice_line_text_rect.x = 9 * SCREENWIDTH / 20
            voice_line_text_rect.y = y
            fonts.GD_FONTS[32].render_to(screen, voice_line_text_rect, line, (255, 255, 255))
            y += 30
    else:
        #when the voiceline number is 5, it calls the handle loan function
        handle_loans()

def handle_loans():
    #draws background and renders sprites
    screen.fill((135, 206, 250))
    screen.blit(contract, ((SCREENWIDTH - 700) / 2, 50))
    screen.blit(signature_surface, (0, 0))
    confirm_sign_button.draw_button(screen)

def draw_shop_skins():
    scan_x = SCREENWIDTH * 0.37
    scan_y = SCREENHEIGHT * 0.18
    for i in range(11):
        skin = pygame.image.load(f"Assets/playerskin0{i+1}.png").convert_alpha()
        skin = pygame.transform.scale(skin, (SCREENWIDTH / 16, SCREENHEIGHT / 8))
        screen.blit(skin, (scan_x, scan_y))
        scan_x += SCREENWIDTH * (1 / 16 + 0.02)
        if (i + 1) % 4 == 0:
            scan_y += SCREENHEIGHT * (0.3925 / 3 + 0.08)
            scan_x = SCREENWIDTH * 0.37
    scan_x = SCREENWIDTH * 0.37
    scan_y = SCREENHEIGHT * 0.18
    screen.blit(shop_border, (scan_x + ((game_screen.skin_num - 1) % 4) * SCREENWIDTH * (1 / 16 + 0.02) - SCREENWIDTH * 0.0085, scan_y + ((game_screen.skin_num - 1) // 4) * (SCREENHEIGHT * (0.3925 / 3 + 0.08)) - SCREENHEIGHT * 0.0275))

def draw_shop_screen():
    screen.fill((8, 123, 255))
    place_chips_on_screen()

    if loan_out:
        pay_loan_button.draw_button(screen)
    else:
        pygame.draw.rect(screen, (0, 85, 210), (SCREENWIDTH * 0.1, SCREENHEIGHT * 0.15, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.6), border_radius=20)
        chip_mult_button.draw_button(screen)
        skin_change_button.draw_button(screen)
        draw_shop_skins()
        player_skin = pygame.image.load(f"Assets/playerskin0{game_screen.skin_num}.png").convert_alpha()
        player_skin = pygame.transform.scale(player_skin, (SCREENWIDTH / 8, SCREENHEIGHT / 4))
        screen.blit(player_skin, (SCREENWIDTH * 0.1675, SCREENHEIGHT * 0.22))
        fonts.GD_FONTS[24].render_to(screen, (chip_mult_button.x + chip_mult_button.w / 3.5, chip_mult_button.y + chip_mult_button.h - 30), f'Currently: x{game_screen.chip_multiplier} Chips', (255, 255, 255))
    screen.blit(shop_shark, (6.5 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 10))
    back_button.draw_button(screen)

def transition_screens(next_screen):
    transition_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    transition_surface.fill((0, 0, 0))

    for alpha in range(0, 255, 15):
        transition_surface.set_alpha(alpha)
        screen.blit(transition_surface)
        pygame.display.flip()
        pygame.time.delay(15)

    for alpha in range(255, -1, -15):
        next_screen()
        transition_surface.set_alpha(alpha)
        screen.blit(transition_surface)
        pygame.display.flip()
        pygame.time.delay(15)

#screen setup, use pygame-ce for best experience
try:
    SCREENWIDTH = (pygame.display.get_desktop_sizes())[0][0]
except AttributeError:
    SCREENWIDTH = 1920
SCREENHEIGHT = SCREENWIDTH * 0.5
print(SCREENWIDTH)
print(SCREENHEIGHT)

#where the top of the floor is (for collision physics principles)
GROUND_Y = math.floor(0.9 * SCREENHEIGHT)

#default size
gd_font_size = 80
gd_font = pygame.freetype.Font("Assets/pusab.otf", gd_font_size)

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync= 1)
bg = pygame.image.load("Assets/background.png").convert()
bg = pygame.transform.scale(bg, (SCREENWIDTH * 1.25, SCREENHEIGHT * 1.25))

#initializes the player
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y, 1)

#initializes buttons
play_button = Button(SCREENWIDTH * 0.4, SCREENHEIGHT * 0.25, SCREENWIDTH * 0.2, SCREENHEIGHT * 0.4, (19, 232, 63), 'Dash', 'GD', 100, (0, 0, 0))
casino_button = Button(SCREENWIDTH * 0.65, SCREENHEIGHT * 0.3, SCREENWIDTH * 0.15, SCREENHEIGHT * 0.3, (229, 27, 53), 'Casino', 'GD', 40, (0, 0, 0))
shop_button = Button(SCREENWIDTH * 0.2, SCREENHEIGHT * 0.3, SCREENWIDTH * 0.15, SCREENHEIGHT * 0.3, (8, 123, 255), 'Shop', 'GD', 40, (0,0,0))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), 'X', "GD", 24, (245, 200, 76))
blackjack_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), 'Blackjack', 'CASINO', 40, (0, 0, 0))
poker_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 4, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), 'Poker', 'CASINO', 40, (0, 0, 0))
continue_button = Button(SCREENWIDTH * 0.4, SCREENHEIGHT * 0.25, SCREENWIDTH * 0.2, SCREENHEIGHT * 0.4, (14, 237, 70), 'Continue', 'GD', 50, (0, 0, 0))
confirm_sign_button = Button(SCREENWIDTH / 15, SCREENHEIGHT / 2, SCREENWIDTH / 4, SCREENHEIGHT / 5, (80, 200, 120), 'Confirm', 'GD', 40, (0, 0, 0))
chip_mult_button = Button(SCREENWIDTH * 0.2, SCREENHEIGHT * 0.8, SCREENWIDTH * 0.4, SCREENHEIGHT * 0.15, (0,0,255), '+1 Chip Mult (10,000)', 'GD', 40, (255,255,255))
chip_mult_button.press = False
skin_change_button = Button(SCREENWIDTH * 0.105, SCREENHEIGHT * 0.54, SCREENWIDTH * 0.25, SCREENHEIGHT * 0.2, (0,0,255), 'Change Skin (1,000)', 'GD', 32, (255,255,255))
skin_change_button.press = False
pay_loan_button = Button(10, SCREENHEIGHT / 2, SCREENWIDTH - 20, SCREENHEIGHT / 2, (255,0,0), 'Pay Back Loan (1,100)', 'GD', 100, (255,255,255))
pay_loan_button.press = False

floor_color = [0,42,124]
chips = 100000000
signature_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
drawing = False
last_signature_pos = None
voice_line_num = 1
current_voice_line = voice_lines[voice_line_num]
player_state = "cube"
game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, GROUND_Y, bg, player_state)
casino_screen = CasinoScreenManager(screen, chips, SCREENWIDTH, SCREENHEIGHT)

# Loads and scales all the images that never change
chips_icon = pygame.image.load("Assets/chipsicon.png").convert_alpha()
chips_icon = pygame.transform.scale(chips_icon, (SCREENWIDTH / 20, SCREENHEIGHT / 10))
contract = pygame.image.load("Assets/loancontract.png").convert_alpha()
contract = pygame.transform.scale(contract, (500, 500))
bank = pygame.image.load("Assets/bank.png").convert_alpha()
bank = pygame.transform.scale(bank, (3 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 5))
loan_shark = pygame.image.load("Assets/loanshark.png").convert_alpha()
loan_shark = pygame.transform.scale(loan_shark, (4 * SCREENWIDTH / 10, 4 * SCREENHEIGHT / 5))
shop_shark = pygame.image.load("Assets/shopshark.png").convert_alpha()
shop_shark = pygame.transform.scale(shop_shark, (SCREENWIDTH * 0.4, SCREENHEIGHT * 0.8))
casino_shark = pygame.image.load("Assets/casinoshark.png").convert_alpha()
casino_shark = pygame.transform.scale(casino_shark, (SCREENWIDTH * 0.4, SCREENHEIGHT * 0.8))
play_icon = pygame.image.load("Assets/playicon.png").convert_alpha()
play_icon = pygame.transform.scale(play_icon, (SCREENWIDTH * 0.15, SCREENHEIGHT * 0.3))
casino_icon = pygame.image.load("Assets/casinoicon.png").convert_alpha()
casino_icon = pygame.transform.scale(casino_icon, (SCREENWIDTH * 0.1, SCREENHEIGHT * 0.2))
shop_icon = pygame.image.load("Assets/shopicon.png").convert_alpha()
shop_icon = pygame.transform.scale(shop_icon, (SCREENWIDTH * 0.1, SCREENHEIGHT * 0.2))
shop_border = pygame.image.load("Assets/shopborder.png").convert_alpha()
shop_border = pygame.transform.scale(shop_border, (SCREENWIDTH / 10, SCREENHEIGHT / 5))
block = pygame.image.load("Assets/gambledashblock.png").convert_alpha()
block = pygame.transform.scale(block, (SCREENWIDTH / 20, SCREENHEIGHT / 10))
spike = pygame.image.load("Assets/spike.png").convert_alpha()
spike = pygame.transform.scale(spike, (100, 100))
spike = pygame.transform.scale(spike, (SCREENWIDTH / 20, SCREENHEIGHT / 10))


pygame.display.set_caption("GambleDash")
running = True
in_menu = True
in_game = False
in_casino = False
in_death_screen = False
in_loan_screen = False
in_shop = False
loan_out = False

while running:
    #event handling
    for event in pygame.event.get():
        #quit events
        if event.type == pygame.QUIT:
            running = False
            
        if in_loan_screen:
            #changes the voice lines when the user hits space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if voice_line_num != 5:
                        voice_line_num += 1
                    current_voice_line = voice_lines[voice_line_num]
            if voice_line_num == 5:
                #lets the user draw on the screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drawing = True
                        last_signature_pos = event.pos
                elif event.type == pygame.MOUSEMOTION:
                    if drawing:
                        if last_signature_pos is not None:
                            pygame.draw.line(signature_surface, (0, 0, 0), last_signature_pos, event.pos, 3)
                        last_signature_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing = False
                        last_signature_pos = None

            if confirm_sign_button.check_button_click(event):
                voice_line_num += 1

            if voice_line_num == 8:
                chips += 1000
                in_menu = True
                in_loan_screen = False
                loan_out = True
                pygame.mixer.music.fadeout(3500)
                signature_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
                drawing = False
                last_signature_pos = None

        if in_menu:
            if play_button.check_button_click(event):
                if chips >= 50:
                    transition_screens(draw_game_screen)
                    in_menu = False
                    in_game = True
                    chips -= 50
                    game_screen.run_chips = 0
                    game_screen.reset_game(game_screen.player)
                else:
                    voice_line_num = 1
                    transition_screens(draw_loan_screen)
                    in_loan_screen = True
                    in_menu = False
                    current_voice_line = voice_lines[voice_line_num]
                    draw_loan_screen()
            if casino_button.check_button_click(event):
                transition_screens(draw_casino_screen)
                in_menu = False
                in_casino = True
                casino_screen.chips = chips
            if shop_button.check_button_click(event):
                transition_screens(draw_shop_screen)
                in_menu = False
                in_shop = True

        if in_casino:
            if blackjack_button.check_button_click(event):
                chips, running = casino_screen.play_blackjack()
            if poker_button.check_button_click(event):
                chips, running = casino_screen.play_poker()
            if back_button.check_button_click(event):
                transition_screens(draw_menu_screen)
                in_casino = False
                in_menu = True

        if in_game:
            if back_button.check_button_click(event):
                transition_screens(draw_menu_screen)
                in_game = False
                in_menu = True

        if in_death_screen:
            pygame.mixer.music.stop()
            if back_button.check_button_click(event):
                transition_screens(draw_menu_screen)
                in_death_screen = False
                in_menu = True
                chips += game_screen.run_chips * game_screen.chip_multiplier
            if casino_button.check_button_click(event):
                transition_screens(draw_casino_screen)
                in_casino = True
                in_death_screen = False
                casino_screen.chips = chips
            if continue_button.check_button_click(event):
                if chips >= 50:
                    chips -= 50
                    transition_screens(draw_game_screen)
                    in_death_screen = False
                    in_game = True
                    game_screen.run_chips = 0
                    game_screen.reset_game(game_screen.player)
                else:
                    transition_screens(draw_loan_screen)
                    in_menu = False
                    in_death_screen = False
                    in_loan_screen = True
                    voice_line_num = 1
                    current_voice_line = voice_lines[voice_line_num]
            if shop_button.check_button_click(event):
                transition_screens(draw_shop_screen)
                in_death_screen = False
                in_shop = True

        if in_shop:
            if loan_out:
                if pay_loan_button.check_button_click(event) and chips >= 1100:
                    chips -= 1100
                    loan_out = False
                    pay_loan_button.press = False
            else:
                if chip_mult_button.check_button_click(event) and chips >= 10000:
                    game_screen.chip_multiplier += 1
                    chips -= 10000
                if skin_change_button.check_button_click(event) and chips >= 1000:
                    old_skin_num = game_screen.skin_num
                    game_screen.skin_num = random.randint(1,10)
                    while game_screen.skin_num == old_skin_num:
                        old_skin_num = game_screen.skin_num
                        game_screen.skin_num = random.randint(1,10)
                    chips -= 1000
            if back_button.check_button_click(event):
                transition_screens(draw_menu_screen)
                in_shop = False
                in_menu = True
                skin_change_button.press = False
                chip_mult_button.press = False

    if in_game:
        # plays music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('Assets/MainTheme.mp3')
            pygame.mixer.music.play(-1)
        draw_game_screen()
        game_screen.tick(player)
        if not game_screen.player_alive:
            chips += game_screen.run_chips * game_screen.chip_multiplier
            in_game = False
            in_death_screen = True

    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()
    elif in_death_screen:
        draw_death_screen()
    elif in_loan_screen:
        # plays music when entering the loan screen
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('Assets/completely_innocent_song.mp3')
            pygame.mixer.music.play(-1)
        draw_loan_screen()
    elif in_shop:
        if loan_out:
            pay_loan_button.press = True
        else:
            chip_mult_button.press = True
            skin_change_button.press = True
        draw_shop_screen()

    pygame.display.flip()