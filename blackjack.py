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
        self.deck = Deck()
        self.deck.shuffle()
        self.chips = chips
        self.bet_amount = 10
        self.is_bet_set = False
        self.chips_added = False

        self.card_back = pygame.image.load('Assets/Cards/0_card_back.png')
        self.card_back = pygame.transform.scale(self.card_back, (70.4, 108.8))
        self.player_hand = []
        self.dealer_hand = []
        self.game = 'blackjack'

    #prints i
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
        bet_less_button = Button(self.screen_width * 0.2, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), ('-10 chips', 'Assets/casino.ttf', 40, (0, 0, 0)))
        set_bet_button = Button(self.screen_width * 0.4, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), (f"Bet {self.bet_amount} chips", 'Assets/casino.ttf', 40, (0, 0, 0)))
        bet_more_button = Button(self.screen_width * 0.6, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), ('+10 chips', 'Assets/casino.ttf', 40, (0, 0, 0)))

        play_again_button.press = False

        player_playing = True
        blackjack_in_game = False
        blackjack_running = True
        while blackjack_running:
            self.surface.fill((16, 82, 9))
            if blackjack_in_game:
                hit_button.press = True
                stand_button.press = True
            else:
                play_again_button.press = True
            if not self.is_bet_set:
                bet_less_button.draw_button(self.surface)
                bet_less_button.render_text(self.surface)
                bet_more_button.draw_button(self.surface)
                bet_more_button.render_text(self.surface)
                set_bet_button.text = f"Bet {self.bet_amount} chips"
                set_bet_button.draw_button(self.surface)
                set_bet_button.render_text(self.surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if hit_button.check_button_click(event):
                    self.player_hand.deal_card(self.deck)
                if stand_button.check_button_click(event):
                    player_playing = False
                if play_again_button.check_button_click(event):
                    self.player_hand = BlackjackHand(self.deck)
                    self.dealer_hand = BlackjackHand(self.deck)
                    player_playing = True
                    play_again_button.press = False
                    hit_button.press = True
                    stand_button.press = True
                    blackjack_running = True
                    self.is_bet_set = False
                    self.chips_added = False
                if bet_less_button.check_button_click(event) and not self.is_bet_set:
                    self.bet_amount -= 10
                    if self.bet_amount < 0: self.bet_amount = 0
                if bet_more_button.check_button_click(event) and not self.is_bet_set:
                    self.bet_amount += 10
                    if self.bet_amount > self.chips: self.bet_amount = self.chips
                if set_bet_button.check_button_click(event) and not self.is_bet_set:
                    self.chips -= self.bet_amount
                    self.is_bet_set = True
                    blackjack_in_game = True
            self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 5), f'Your Chips: {self.chips}', (255, 255, 255))
            if self.is_bet_set:
                if player_playing:
                    self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 4), f'Hand Value: {self.player_hand.get_hand_value()}', (255, 255, 255))
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
                        if not self.chips_added:
                            self.chips += self.bet_amount * 2
                            self.chips_added = True
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
                        self.dealer_hand.deal_card(self.deck)
                    if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                        self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'You Win!', (255, 255, 255))
                        if not self.chips_added:
                            self.chips += self.bet_amount * 2
                            self.chips_added = True
                    elif player_hand_value == dealer_hand_value:
                        self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'Push!', (255, 255, 255))
                    else:
                        self.fonts[100].render_to(self.surface, (self.screen_width / 4, self.screen_height / 2.3), 'You Lose!', (255, 255, 255))
            pygame.display.flip()