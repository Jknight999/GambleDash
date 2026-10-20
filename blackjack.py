import random
import pygame
from time import sleep
import pygame.freetype
from game_classes import Button

pygame.init()
pygame.freetype.init()

CASINO_FONTS = {
    14: pygame.freetype.Font('Assets/casino.ttf', 14),
    18: pygame.freetype.Font('Assets/casino.ttf', 18),
    24: pygame.freetype.Font('Assets/casino.ttf', 24),
    32: pygame.freetype.Font('Assets/casino.ttf', 32),
    50: pygame.freetype.Font('Assets/casino.ttf', 50),
    100: pygame.freetype.Font('Assets/casino.ttf', 100)
}

SCREENHEIGHT = 500
SCREENWIDTH = 1000
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync= 1)

#this is the file to create the gambling
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f"Assets/Cards/{self.rank}of{self.suit}.png")
        self.image = pygame.transform.scale(self.image, (70.4, 108.8))

    #basically just represents it as a string (for printing purposes)
    def __repr__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        suits = ("Hearts", "Diamonds", "Spades", "Crosses")
        ranks = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
        # list comprehension stuff -- but basically just initializes a card for each suit and rank by looping through their iterables
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    #takes a card off the top
    def deal(self):
        if len(self.cards) == 0:
            self.__init__()
        return self.cards.pop()

    #shuffles the cards randomly - just used it to improve readability
    def shuffle(self):
        random.shuffle(self.cards)

#for input validation later on
blackjack_possible_actions = {'hit', 'stand', 'double'}
supported_games = {'blackjack'}

#dictionary mapping card ranks to card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
}

#calculates the value of a hand
def calculate_hand(hand):
    #more list comp -- just translates the cards into their numerical values using the dict
    current_values = [card_values[s.rank] for s in hand]
    #so that we can take care of aces last
    current_values.sort()
    hand_value = 0
    #iterates through each value
    for value in current_values:
        #everything except for aces
        if value != 11:
            hand_value += value
        #just checks if adding and ace would make the hand bust
        elif hand_value < 11:
            hand_value += value
        else: hand_value += 1
    #returns the calculated value -- so CATCH IT
    return hand_value

#initializes the first deck -- we may need more
my_deck = Deck()
my_deck.shuffle()

#starting amount of chips - we need to set this to whatever they got from geo dash whenever we insert it
chips = 100
card_back = pygame.image.load('Assets/Cards/0_card_back.png')
card_back = pygame.transform.scale(card_back, (70.4, 108.8))

#prints
def print_player_hand(p_hand, x, y, spacer):
    global screen
    i = x - (len(p_hand) * p_hand[0].image.get_width() / 2) - (spacer * len(p_hand) // 2)
    for card in p_hand:
        screen.blit(card.image, (i, y))
        i += card.image.get_width() + spacer

def print_dealer_start_hand(d_hand, x, y, spacer):
    global screen
    i = x - (len(d_hand) * d_hand[0].image.get_width() / 2) - (spacer * len(d_hand) // 2)
    for card in d_hand:
        if card != d_hand[-1]:
            screen.blit(card.image, (i, y))
        else:
            screen.blit(card_back, (i, y))
        i += card.image.get_width() + spacer

def blackjack_start_hand():
    hand = []
    for _ in range(2):
        hand.append(my_deck.deal())
    return hand

player_hand = blackjack_start_hand()
dealer_hand = blackjack_start_hand()
hit_button = Button(SCREENWIDTH * 0.8, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 8, SCREENHEIGHT / 5, (255, 0, 0), ('Hit', 'Assets/casino.ttf', 40, (0, 0, 0)))
stand_button = Button(SCREENWIDTH * 0.1, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 8, SCREENHEIGHT / 5, (255,0,0), ('Stand', 'Assets/casino.ttf', 40, (0,0,0)))
play_again_button = Button(SCREENWIDTH * 0.7, SCREENHEIGHT / 2 + SCREENHEIGHT / 6, SCREENWIDTH / 5, SCREENHEIGHT / 5, (255, 0, 0), ('Play Again', 'Assets/casino.ttf', 40, (0, 0, 0)))
play_again_button.press = False

player_playing = True
running = True
in_main_menu = True
while running:
    screen.fill((16, 82, 9))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if hit_button.check_button_click(event):
            player_hand.append(my_deck.deal())
        if stand_button.check_button_click(event):
            player_playing = False
        if play_again_button.check_button_click(event):
            player_hand = blackjack_start_hand()
            dealer_hand = blackjack_start_hand()
            player_playing = True
            play_again_button.press = False
            hit_button.press = True
            stand_button.press = True
    player_hand_value = calculate_hand(player_hand)
    dealer_hand_value = calculate_hand(dealer_hand)
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 5), f'Your Chips: {chips}', (255, 255, 255))
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 4), f'Hand Value: {player_hand_value}', (255, 255, 255))
    if player_playing:
        if player_hand_value > 21:
            screen.fill((0,0,0))
            CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), f'You Busted',(255, 255, 255))
            chips -= 50
            play_again_button.press = True
            hit_button.press = False
            stand_button.press = False
            play_again_button.draw_button(screen)
            play_again_button.render_text(screen)
        elif player_hand_value == 21:
            screen.fill((0, 0, 0))
            CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), f'Blackjack!', (255, 255, 255))
            chips += 50
            play_again_button.press = True
            hit_button.press = False
            stand_button.press = False
            play_again_button.draw_button(screen)
            play_again_button.render_text(screen)
        else:
            hit_button.draw_button(screen)
            hit_button.render_text(screen)
            stand_button.draw_button(screen)
            stand_button.render_text(screen)

            print_player_hand(player_hand, 500, 300, 5)
            print_dealer_start_hand(dealer_hand, 500, 50, 5)
    else:
        play_again_button.press = True
        hit_button.press = False
        stand_button.press = False
        play_again_button.draw_button(screen)
        play_again_button.render_text(screen)
        print_player_hand(player_hand, 500, 300, 5)
        print_player_hand(dealer_hand, 500, 50, 5)
        while dealer_hand_value < 17:
            dealer_hand.append(my_deck.deal())
            dealer_hand_value = calculate_hand(dealer_hand)
        if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
            chips += 50
            CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), 'You Win!', (255, 255, 255))
        else:
            chips -= 50
            CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), 'You Lose!', (255, 255, 255))
    pygame.display.flip()