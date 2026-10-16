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

    #takes a card off the top
    def deal(self):
        if len(self.cards) == 0:
            return None
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

player_playing = True
running = True
while running:
    screen.fill((16, 82, 9))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if hit_button.check_button_click(event):
            player_hand.append(my_deck.deal())
        if stand_button.check_button_click(event):
            player_playing = False
    player_hand_value = calculate_hand(player_hand)
    dealer_hand_value = calculate_hand(dealer_hand)
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 5), f'Your Chips: {chips}', (255, 255, 255))
    CASINO_FONTS[18].render_to(screen, (SCREENWIDTH / 15, SCREENHEIGHT / 4), f'Hand Value: {player_hand_value}', (255, 255, 255))
    if player_playing:
        if player_hand_value > 21:
            screen.fill((0,0,0))
            CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), f'You Busted',(255, 255, 255))
        else:
            hit_button.draw_button(screen)
            hit_button.render_text(screen)
            stand_button.draw_button(screen)
            stand_button.render_text(screen)

            print_player_hand(player_hand, 500, 300, 5)
            print_dealer_start_hand(dealer_hand, 500, 50, 5)
    elif not player_playing:
        print_player_hand(player_hand, 500, 300, 5)
        print_player_hand(dealer_hand, 500, 50, 5)
        if dealer_hand_value <= 16:
            dealer_hand.append(my_deck.deal())
        else:
            if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), 'You Win!', (255, 255, 255))
            else:
                CASINO_FONTS[100].render_to(screen, (SCREENWIDTH / 4, SCREENHEIGHT / 2.3), 'You Lose!', (255, 255, 255))

    pygame.display.flip()

#actual 'game loop'
'''
while chips > 0:
    #blackjack game
    if current_game == 'blackjack':
        #just to make it look nice
        print(f"=======BLACKJACK=======\nYou have {chips} chips.")

        bet = input("How many chips would you like to bet? ")
        #input validation for the bet (must be a whole number less than or equal to their number of chips)
        #you can cast to int since it exits the statement immediately if isdigit() evaluates to False
        while not (bet.isdigit() and 0 < int(bet) <= chips):
            bet = input("Invalid Input. How many chips would you like to bet? ")
        bet = int(bet)

        #deals in the player
        player_hand = blackjack_start_hand()
        print_player_hand()
        player_playing = True

        #deals in the dealer
        dealer_hand = blackjack_start_hand()
        dealer_hand_value = calculate_hand(dealer_hand)
        print_dealer_hand()
        dealer_playing = True

        #actual player-interactive loop
        while player_playing:
            player_action = input('What would you like to do (hit, stand, double)? ').lower()
            #input validation for action
            while player_action not in blackjack_possible_actions:
                player_action = input('Invalid Action. What would you like to do (hit, stand, double)? ')

            #what happens for each action
            if player_action == 'hit':
                player_hand.append(my_deck.deal())
                print_player_hand()
            elif player_action == 'stand':
                player_hand_value = calculate_hand(player_hand)
                player_playing = False
            elif player_action == 'double':
                bet *= 2
                player_hand.append(my_deck.deal())
                print_player_hand()
                player_hand_value = calculate_hand(player_hand)
                player_playing = False

            #calculates hand value and checks if they busted (the dealer won't have to play)
            player_hand_value = calculate_hand(player_hand)
            if player_hand_value > 21:
                print("You busted.")
                dealer_playing = False
                break

        #only plays if the player didn't bust
        while dealer_playing:
            dealer_hand_value = calculate_hand(dealer_hand)
            if dealer_hand_value <= 16:
                dealer_hand.append(my_deck.deal())
            elif dealer_hand_value == 17 and 'A' in dealer_hand:
                dealer_hand.append(my_deck.deal())
            else:
                dealer_playing = False

        #checks all the possible outcomes for the player hand in relation to the dealer's hand
        #I really don't know how it could possibly be undefined, see if you can figure it out
        if player_hand_value <= 21:
            print("Dealer Hand: ", end='')
            for i in range(len(dealer_hand)):
                print(dealer_hand[i], end=' ')
            print('')
        if player_hand_value > 21:
            chips -= bet
        elif 22 > dealer_hand_value > player_hand_value:
            print("You lose.")
            chips -= bet
        elif dealer_hand_value == player_hand_value:
            print("Push.")
        else:
            print("You win.")
            chips += bet

    #checks if they want to keep going or change to a different game
    if chips == 0:
        break
    try_again = input(f'Would you like to keep playing {current_game} or try another of our supported games?\nType "keep going" to remain playing and "try another" if you would like to try your luck at a different game. ').lower()

    #input validation
    while try_again != 'keep going' and try_again != 'try another':
        try_again = input(f'Invalid Input. Type "keep going" to remain playing and "try another" if you would like to try your luck at a different game. ').lower()

    #either keeps playing or prompts them for the new game they would like to play
    if try_again == 'keep going':
        pass
    else:
        print('What casino game would you like to play?\nCurrently supported games: ', end='')
        for game in supported_games:
            print(game, end=' ')
        current_game = input('').lower()
        while current_game.lower() not in supported_games:
            current_game = input('That game is currently not supported. Please enter the name of a supported game: ').lower()
    '''