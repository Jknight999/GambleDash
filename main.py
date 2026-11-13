#imports
import pygame
import pygame.freetype
import math
import fonts

from game_classes import Player, Button
from game_screen_manager import GameScreenManager
from casino_screen_manager import CasinoScreenManager
from loan_shark_voice_lines import voice_lines

#inits
pygame.init()
pygame.mixer.init()
pygame.freetype.init()

#screen drawing functions
def draw_menu_screen():
    draw_game_screen()
    
    #takes the players chips and renders it to the screen
    chip_text = str(chips)
    text_rect = fonts.GD_FONTS[50].get_rect(chip_text)
    text_rect.right = SCREENWIDTH - 70
    fonts.GD_FONTS[50].render_to(screen, text_rect, chip_text, (255, 255, 255))
    chips_icon = pygame.image.load("Assets/chipsicon.png").convert_alpha()
    screen.blit(chips_icon, (SCREENWIDTH - 60, 30))

    #draws play and casino buttons
    play_button.draw_button(screen)
    casino_button.draw_button(screen)
    upgrade_button.draw_button(screen)

def draw_casino_screen():
    #handles screen background and text
    screen.fill((94, 6, 6))
    fonts.CASINO_FONTS[50].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 7), 'Casino', (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREENWIDTH, SCREENHEIGHT), width=math.floor(SCREENWIDTH / 20))
    
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

def draw_death_screen(chipnum):
    if not game_screen.player_alive:
        #resets run chips and renders chips to the screen
        game_screen.run_chips = 0
        chip_text = str(chipnum)
        text_rect = fonts.GD_FONTS[50].get_rect(chip_text)
        text_rect.right = SCREENWIDTH - 70
        fonts.GD_FONTS[50].render_to(screen, text_rect, chip_text, (255, 255, 255))
        chips_icon = pygame.image.load("Assets/chipsicon.png").convert_alpha()
        screen.blit(chips_icon, (SCREENWIDTH - 60, 30))
        
        #draws back, continue, and casino buttons
        back_button.draw_button(screen)
        continue_button.draw_button(screen)
        casino_button.draw_button(screen)
        upgrade_button.draw_button(screen)

def draw_loan_screen():
    #plays music when entering the loan screen
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('Assets/completely_innocent_song.mp3')
        pygame.mixer.music.play(-1)
        
    if voice_line_num != 5:
        #handles background, text, and sprites
        screen.fill((135, 206, 250))
        pygame.draw.rect(screen, (126, 200, 80), (0, 2 * SCREENHEIGHT / 3, SCREENWIDTH, SCREENHEIGHT / 2.9))
        bank = pygame.image.load("Assets/bank.png").convert_alpha()
        bank = pygame.transform.scale(bank, (3 * SCREENWIDTH / 10, 3 * SCREENHEIGHT / 5))
        loan_shark = pygame.image.load("Assets/loanshark.png").convert_alpha()
        loan_shark = pygame.transform.scale(loan_shark, (4 * SCREENWIDTH / 10, 4 * SCREENHEIGHT / 5))
        screen.blit(bank, (SCREENWIDTH / 10, SCREENHEIGHT / 5))
        screen.blit(loan_shark, (SCREENWIDTH - 350, SCREENHEIGHT - 300))
        voice_line_text = current_voice_line
        voice_line_text_rect = fonts.GD_FONTS[18].get_rect(voice_line_text)
        voice_line_text_rect.x = 300
        voice_line_text_rect.y = 100
        
        #places the voice lines so that they are written in lines to the screen
        lines = current_voice_line.split("\n")
        y = voice_line_text_rect.y
        for line in lines:
            voice_line_text_rect = fonts.GD_FONTS[32].get_rect(line)
            voice_line_text_rect.x = 450
            voice_line_text_rect.y = y
            fonts.GD_FONTS[32].render_to(screen, voice_line_text_rect, line, (255, 255, 255))
            y += 30
    else:
        #when the voiceline number is 5, it calls the handle loan function
        handle_loans()

def handle_loans():
    #draws background and renders sprites
    screen.fill((135, 206, 250))
    contract = pygame.image.load("Assets/loancontract.png").convert_alpha()
    contract = pygame.transform.scale(contract, (500, 500))
    screen.blit(contract, ((SCREENWIDTH - 700) / 2, 50))
    screen.blit(signature_surface, (0, 0))

def draw_upgrade_screen():
    screen.fill((0,128,0))


#screen setup
SCREENWIDTH = pygame.display.get_desktop_sizes()[0][0]
SCREENHEIGHT = SCREENWIDTH * 0.5
#where the top of the floor is (for collision physics principles)
GROUND_Y = math.floor(0.7 * SCREENHEIGHT)

#default size
gd_font_size = 80
gd_font = pygame.freetype.Font("Assets/pusab.otf", gd_font_size)

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync= 1)
bg = pygame.image.load("assets/background.png").convert()
bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))

#initializes the player
player = Player(SCREENWIDTH, SCREENHEIGHT, GROUND_Y)

#I have absolutely no idea why but this is necessary to make the cube start the right way up
player.angle = 91
player.rotated_surface = pygame.transform.rotate(player.image, player.angle)
player.rect = player.rotated_surface.get_rect(center=(player.x + player.w // 2, player.y + player.h // 2))

#initializes buttons
play_button = Button(SCREENWIDTH / 5, SCREENHEIGHT / 6, SCREENWIDTH * 0.6, SCREENHEIGHT * 0.4, (14, 237, 70), 'Dash', 'GD', 100, (255, 255, 255))
casino_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2 + SCREENHEIGHT / 4, SCREENWIDTH / 3, SCREENHEIGHT / 5, (94, 6, 6), 'Gamble', 'CASINO', 80, (0, 0, 0))
back_button = Button(SCREENHEIGHT / 20, SCREENWIDTH / 40, SCREENHEIGHT / 10, SCREENWIDTH / 20, (14, 237, 70), 'X', "GD", 24, (245, 200, 76))
blackjack_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 2, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), 'Blackjack', 'CASINO', 40, (0, 0, 0))
poker_button = Button(SCREENWIDTH / 3, SCREENHEIGHT / 4, SCREENWIDTH / 3, SCREENHEIGHT / 5, (255, 0, 0), 'Poker', 'CASINO', 40, (0, 0, 0))
continue_button = Button(SCREENWIDTH / 4, SCREENHEIGHT / 4, SCREENWIDTH / 2, SCREENHEIGHT / 5, (14, 237, 70), 'Continue for 50 Chips?', 'GD', 40, (0, 0, 0))
shop_button = Button(SCREENWIDTH / 15, SCREENHEIGHT / 2 + SCREENHEIGHT / 4, SCREENWIDTH / 4, SCREENHEIGHT / 5, (0,0,255), 'Shop', 'GD', 40, (0,0,0))
chip_mult_button = Button(SCREENWIDTH / 15, SCREENHEIGHT / 2 + SCREENHEIGHT / 4, SCREENWIDTH / 4, SCREENHEIGHT / 5, (0,0,255), '+1 Chip Mult (100)', 'GD', 40, (0,0,0))

floor_color = [0,42,124]
chips = 100
signature_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
drawing = False
last_signature_pos = None
voice_line_num = 1
current_voice_line = voice_lines[voice_line_num]
player_state = "cube"
game_screen = GameScreenManager(screen, player, SCREENWIDTH, SCREENHEIGHT, floor_color, GROUND_Y, bg, player_state)
casino_screen = CasinoScreenManager(screen, chips, SCREENWIDTH, SCREENHEIGHT)

pygame.display.set_caption("GambleDash")
running = True
in_menu = True
in_game = False
in_casino = False
in_death_screen = False
in_loan_screen = False
in_shop = False

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
                    if voice_line_num < 5:
                        voice_line_num += 1
                    elif voice_line_num >= 8:
                        in_loan_screen = False
                        in_menu = True
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

        if in_menu:
            if play_button.check_button_click(event):
                if chips >= 50:
                    in_menu = False
                    in_game = True
                    chips -= 50
                    game_screen.run_chips = 0
                    game_screen.reset_game(game_screen.player)
                else:
                    voice_line_num = 1
                    in_loan_screen = True
                    in_menu = False
                    current_voice_line = voice_lines[voice_line_num]
                    draw_loan_screen()
            if casino_button.check_button_click(event):
                in_menu = False
                in_casino = True

        if in_casino:
            if blackjack_button.check_button_click(event):
                chips, running = casino_screen.play_blackjack()
            if poker_button.check_button_click(event):
                casino_screen.play_poker()
            if back_button.check_button_click(event):
                in_casino = False
                in_menu = True

        if in_game:
            if back_button.check_button_click(event):
                in_game = False
                in_menu = True

        if in_death_screen:
            if back_button.check_button_click(event):
                in_death_screen = False
                in_menu = True
                chips += game_screen.run_chips * game_screen.chip_multiplier
            if casino_button.check_button_click(event):
                in_casino = True
                in_death_screen = False
                casino_screen.chips = chips
            if continue_button.check_button_click(event):
                if chips >= 50:
                    chips -= 50
                    in_death_screen = False
                    in_game = True
                    game_screen.run_chips = 0
                    game_screen.reset_game(game_screen.player)
                else:
                    in_menu = False
                    in_death_screen = False
                    in_loan_screen = True
                    voice_line_num = 1
                    current_voice_line = voice_lines[voice_line_num]

    if in_game:
        draw_game_screen()
        game_screen.tick(player)
        if not game_screen.player_alive:
            draw_game_screen()
            in_game = False
            chips += game_screen.run_chips
            in_death_screen = True
    elif in_casino:
        draw_casino_screen()
    elif in_menu:
        draw_menu_screen()
    elif in_death_screen:
        draw_death_screen(chips)
    elif in_loan_screen:
        draw_loan_screen()

    pygame.display.flip()