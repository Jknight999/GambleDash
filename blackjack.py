import pygame
import pygame.freetype
import sys

from game_classes import Button
from casino_classes import Deck, BlackjackHand

class CasinoScreenManager:
    def __init__(self, screen_to_draw, chips, s_w, s_h):
        self.surface = screen_to_draw
        self.screen_width = s_w
        self.screen_height = s_h

        self.fonts = {
            14: pygame.freetype.Font('Assets/casino.ttf', 14),
            18: pygame.freetype.Font('Assets/casino.ttf', 18),
            24: pygame.freetype.Font('Assets/casino.ttf', 24),
            32: pygame.freetype.Font('Assets/casino.ttf', 32),
            50: pygame.freetype.Font('Assets/casino.ttf', 50),
            100: pygame.freetype.Font('Assets/casino.ttf', 100)
        }
        self.blackjack_possible_actions = {'hit', 'stand', 'double'}
        self.supported_games = {'blackjack'}


        #dictionary mapping card ranks to card values
        self.deck = Deck().shuffle()
        self.chips = chips

        self.card_back = pygame.image.load('Assets/Cards/0_card_back.png')
        self.card_back = pygame.transform.scale(self.card_back, (70.4, 108.8))
        self.player_hand = []
        self.dealer_hand = []
        self.game = 'blackjack'

    #prints
    def print_player_hand(self, p_hand, x, y, spacer):
        i = x - (len(p_hand) * p_hand[0].image.get_width() / 2) - (spacer * len(p_hand) // 2)
        for card in p_hand:
            self.surface.blit(card.image, (i, y))
            i += card.image.get_width() + spacer

    def print_dealer_start_hand(self, d_hand, x, y, spacer):
        i = x - (len(d_hand) * d_hand[0].image.get_width() / 2) - (spacer * len(d_hand) // 2)
        for card in d_hand:
            if card != d_hand[-1]:
                self.surface.blit(card.image, (i, y))
            else:
                self.surface.blit(self.card_back, (i, y))
            i += card.image.get_width() + spacer

    def play_blackjack(self):
        self.player_hand = BlackjackHand(self.deck)
        self.dealer_hand = BlackjackHand(self.deck)

        hit_button = Button(self.screen_width * 0.8, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), ('Hit', 'Assets/casino.ttf', 40, (0, 0, 0)))
        stand_button = Button(self.screen_width * 0.1, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255,0,0), ('Stand', 'Assets/casino.ttf', 40, (0,0,0)))
        play_again_button = Button(self.screen_width * 0.7, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 5, self.screen_height / 5, (255, 0, 0), ('Play Again', 'Assets/casino.ttf', 40, (0, 0, 0)))
        play_again_button.press = False

        player_playing = True
        blackjack_in_game = True
        blackjack_running = True
        while blackjack_running:
            self.surface.fill((16, 82, 9))
            if blackjack_in_game:
                hit_button.press = True
                stand_button.press = True
            else:
                play_again_button.press = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if hit_button.check_button_click(event):
                    self.player_hand.deal_card(self.deck)
                if stand_button.check_button_click(event):
                    player_playing = False
                if play_again_button.check_button_click(event):
                    player_hand = BlackjackHand(self.deck)
                    dealer_hand = BlackjackHand(self.deck)
                    player_playing = True
                    play_again_button.press = False
                    hit_button.press = True
                    stand_button.press = True
                    blackjack_running = True
            self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 5), f'Your Chips: {self.chips}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 4), f'Hand Value: {self.player_hand.get_hand_value()}', (255, 255, 255))
            if player_playing:
                player_hand_value = self.player_hand.get_hand_value()
                if self.player_hand.get_hand_value() > 21:
                    self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), f'You Busted',(255, 255, 255))
                    play_again_button.press = True
                    hit_button.press = False
                    stand_button.press = False
                    play_again_button.draw_button(self.surface)
                    play_again_button.render_text(self.surface)
                    self.print_player_hand(self.player_hand.cards, 500, 300, 5)
                elif player_hand_value == 21:
                    self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), f'Blackjack!', (255, 255, 255))
                    play_again_button.press = True
                    hit_button.press = False
                    stand_button.press = False
                    play_again_button.draw_button(self.surface)
                    play_again_button.render_text(self.surface)
                    self.print_player_hand(self.player_hand.cards, 500, 300, 5)
                    self.print_dealer_start_hand(self.dealer_hand.cards, 500, 50, 5)
                else:
                    hit_button.draw_button(self.surface)
                    hit_button.render_text(self.surface)
                    stand_button.draw_button(self.surface)
                    stand_button.render_text(self.surface)

                    self.print_player_hand(self.player_hand.cards, 500, 300, 5)
                    self.print_dealer_start_hand(self.dealer_hand.cards, 500, 50, 5)
            else:
                play_again_button.press = True
                hit_button.press = False
                stand_button.press = False
                play_again_button.draw_button(self.surface)
                play_again_button.render_text(self.surface)
                self.print_player_hand(self.player_hand.cards, 500, 300, 5)
                self.print_player_hand(self.dealer_hand.cards, 500, 50, 5)
                dealer_hand_value = self.dealer_hand.get_hand_value()
                player_hand_value = self.player_hand.get_hand_value()
                while self.dealer_hand.get_hand_value() < 17:
                    self.dealer_hand.append(self.deck.deal())
                if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                    self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'You Win!', (255, 255, 255))
                elif player_hand_value == dealer_hand_value:
                    self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'Push!', (255, 255, 255))
                else:
                    self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'You Lose!', (255, 255, 255))
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

        #checks all the possible outcomes for the player hand compared to the dealer's hand
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