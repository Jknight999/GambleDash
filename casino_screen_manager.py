#imports
import pygame
import pygame.freetype
import random
from game_classes import Button
from casino_classes import Deck, BlackjackHand, CommunityCards, PokerCPU, PokerPlayer

class CasinoScreenManager:
    def __init__(self, screen_to_draw, chips, s_w, s_h):
        #passes in the screen, screen width, and screen height
        self.surface = screen_to_draw
        self.screen_width = s_w
        self.screen_height = s_h

        #fonts to be used in casino stored in a dict for easier reference
        self.fonts = {
            14: pygame.freetype.Font('Assets/casino.ttf', 14),
            18: pygame.freetype.Font('Assets/casino.ttf', 18),
            24: pygame.freetype.Font('Assets/casino.ttf', 24),
            32: pygame.freetype.Font('Assets/casino.ttf', 32),
            50: pygame.freetype.Font('Assets/casino.ttf', 50),
            100: pygame.freetype.Font('Assets/casino.ttf', 100)
        }

        self.poker_card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }

        self.poker_hand_rankings = {
            "High Card": 1,
            "One Pair": 2,
            "Two Pair": 3,
            "Three of a Kind": 4,
            "Straight": 5,
            "Flush": 6,
            "Full House": 7,
            "Four of a Kind": 8,
            "Straight Flush": 9,
        }

        #initializes and shuffles deck
        self.deck = Deck()
        self.deck.shuffle()

        #gets chips passed in
        self.chips = chips

        #sets default bet amount
        self.bet_amount = 0
        self.is_bet_set = False
        self.chips_added = False

        #creates image for hidden card
        self.card_back = pygame.image.load('Assets/Cards/0_card_back.png')
        self.card_back = pygame.transform.scale(self.card_back, (352 / (self.screen_width / 400), 544 / (self.screen_width / 400)))

        #initializes empty hands for both player and dealer
        self.player_hand = []
        self.dealer_hand = []
        self.community_cards = []

        #sets the game to be played
        self.betting_round = 0

        self.player_hand_value = None

        self.poker_player = PokerPlayer(self.deck, 0, 'Player')

        self.cpu_1 = PokerCPU(self.deck, 0, 'CPU1')
        self.cpu_2 = PokerCPU(self.deck, 0, 'CPU2')
        self.cpu_3 = PokerCPU(self.deck, 0, 'CPU3')

        self.cpus = [self.cpu_1, self.cpu_2, self.cpu_3]

        self.cpu_hands = [self.cpu_1.hand, self.cpu_2.hand, self.cpu_3.hand]

        self.poker_players = [self.poker_player, self.cpu_1, self.cpu_2, self.cpu_3]

    #prints the hand
    def print_player_hand(self, p_hand, x, y, spacer):
        #starts the hand at the fully left position
        i = x - (len(p_hand) * p_hand[0].image.get_width() / 2) - (spacer * len(p_hand) // 2)
        for card in p_hand:
            #draws the card
            self.surface.blit(card.image, (i, y))
            #increments the card by the width of the card plus the spacer value
            i += card.image.get_width() + spacer

    def print_dealer_start_hand(self, d_hand, x, y, spacer):
        #starts the hand at the fully left position
        i = x - (len(d_hand) * d_hand[0].image.get_width() / 2) - (spacer * len(d_hand) // 2)
        for card in d_hand:
            #if it is not the last card in the hand, draw
            if card != d_hand[-1]:
                self.surface.blit(card.image, (i, y))
            #otherwise, draw the back of a card (hidden card)
            else:
                self.surface.blit(self.card_back, (i, y))
            #increments the card by the width of the card plus the spacer value
            i += card.image.get_width() + spacer

    def play_blackjack(self):
        #initializes new instances of the class BlackjackHand (imported from casino_classes)
        #hand already initialized as an empty list
        self.player_hand = BlackjackHand(self.deck)
        self.dealer_hand = BlackjackHand(self.deck)

        #initializes all the buttons
        hit_button = Button(self.screen_width * 0.8, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), 'Hit', 'CASINO', 40, (0, 0, 0))
        stand_button = Button(self.screen_width * 0.1, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255,0,0), 'Stand', 'CASINO', 40, (0,0,0))
        play_again_button = Button(self.screen_width * 0.8, self.screen_height * 0.66, self.screen_width / 5, self.screen_height / 5, (255, 0, 0), 'Play Again?', 'CASINO', 40, (0, 0, 0))
        bet_less_button = Button(self.screen_width * 0.2, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), '-10 chips', 'CASINO', 40, (0, 0, 0))
        set_bet_button = Button(self.screen_width * 0.4, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), f"Bet {self.bet_amount} chips", 'CASINO', 40, (0, 0, 0))
        bet_more_button = Button(self.screen_width * 0.6, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), '+10 chips', 'CASINO', 40, (0, 0, 0))
        back_button = Button(self.screen_width / 20, self.screen_width / 40, self.screen_height / 10, self.screen_width / 20, (14, 237, 70), 'X', "GD", 40, (245, 200, 76))

        #removes the ability to press play again button before the game starts
        play_again_button.press = False

        #if the player is actively playing (not the dealer)
        player_playing = True
        #if the player has the ability to perform actions (hit/stand) (are you on the game screen)
        blackjack_in_game = False
        #if the program is running (modifying bet, playing, or final result
        blackjack_running = True
        win_state = ''
        #game loop

        while blackjack_running:
            #fills the background
            self.surface.fill((16, 82, 9))
            #evaluates whether in_game for button presses (hit/stand is available if in_game, otherwise play_again is viable)
            self.fonts[100].render_to(self.surface, (self.screen_width / 3, self.screen_height / 2.7), f'{win_state}',(255, 255, 255))
            if blackjack_in_game:
                hit_button.press = True
                stand_button.press = True
            else:
                hit_button.press = False
                stand_button.press = False
                play_again_button.press = True

            #allowing bet changes until the bet is set
            if not self.is_bet_set:
                bet_less_button.draw_button(self.surface)
                bet_more_button.draw_button(self.surface)
                set_bet_button.text = f"Bet {self.bet_amount} chips"
                set_bet_button.draw_button(self.surface)

            #figure how to get events and pass them in, perhaps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.chips, False
                #deals a card if the player hits
                if hit_button.check_button_click(event):
                    self.player_hand.deal_card(self.deck)
                if stand_button.check_button_click(event):
                    player_playing = False
                    blackjack_in_game = False
                if play_again_button.check_button_click(event):
                    #resets player hand and dealer hand by initializing new instances of the BlackjackHand class (from casino_classes)
                    self.player_hand = BlackjackHand(self.deck)
                    self.dealer_hand = BlackjackHand(self.deck)
                    player_playing = True
                    play_again_button.press = False
                    blackjack_in_game = True
                    self.is_bet_set = False
                    self.chips_added = False
                    win_state = ''
                if back_button.check_button_click(event):
                    return self.chips, True

                #these three all set the bet amount
                if bet_less_button.check_button_click(event) and not self.is_bet_set:
                    self.bet_amount -= 10
                    if self.bet_amount < 0:
                        self.bet_amount = 0
                if bet_more_button.check_button_click(event) and not self.is_bet_set:
                    self.bet_amount += 10
                    if self.bet_amount > self.chips:
                        self.bet_amount = self.chips
                if set_bet_button.check_button_click(event) and not self.is_bet_set:
                    self.chips -= self.bet_amount
                    self.is_bet_set = True
                    back_button.press = False
                    blackjack_in_game = True

            #always renders how many chips you have
            self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 5), f'Your Chips: {self.chips}', (255, 255, 255))
            if self.is_bet_set:
                if player_playing:
                    #only renders your hand value if you have set your bet to prevent cheating
                    self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 4), f'Hand Value: {self.player_hand.get_hand_value()}', (255, 255, 255))
                    player_hand_value = self.player_hand.get_hand_value()

                    #checks busting
                    if self.player_hand.get_hand_value() > 21:
                        win_state = 'You busted'
                        if self.bet_amount > self.chips:
                            self.bet_amount = self.chips
                        play_again_button.press = True
                        blackjack_in_game = False
                        back_button.press = True
                        back_button.draw_button(self.surface)
                        play_again_button.draw_button(self.surface)
                        self.print_player_hand(self.player_hand.cards, self.screen_width / 2, self.screen_height / 2, 5)
                    #checks blackjacks
                    elif player_hand_value == 21:
                        win_state = 'Blackjack!'
                        if not self.chips_added:
                            self.chips += self.bet_amount * 2
                            self.chips_added = True
                        play_again_button.press = True
                        blackjack_in_game = False
                        play_again_button.draw_button(self.surface)
                        self.print_player_hand(self.player_hand.cards, self.screen_width / 2, self.screen_height / 2, 5)
                        self.print_dealer_start_hand(self.dealer_hand.cards, self.screen_width / 2, self.screen_height / 10, 5)
                    else:
                        hit_button.draw_button(self.surface)
                        stand_button.draw_button(self.surface)

                        self.print_player_hand(self.player_hand.cards, self.screen_width / 2, self.screen_height / 2, 5)
                        self.print_dealer_start_hand(self.dealer_hand.cards, self.screen_width / 2, self.screen_height / 10, 5)

                #this runs when the player stands, starts the dealer's turn
                else:
                    play_again_button.press = True
                    hit_button.press = False
                    stand_button.press = False
                    back_button.press = True
                    play_again_button.draw_button(self.surface)
                    back_button.draw_button(self.surface)
                    self.print_player_hand(self.player_hand.cards, self.screen_width / 2, self.screen_height / 2, 5)
                    self.print_player_hand(self.dealer_hand.cards, self.screen_width / 2, self.screen_height / 10, 5)
                    dealer_hand_value = self.dealer_hand.get_hand_value()
                    player_hand_value = self.player_hand.get_hand_value()

                    #the dealer hits below 17
                    while dealer_hand_value < 17:
                        self.dealer_hand.deal_card(self.deck)
                        dealer_hand_value = self.dealer_hand.get_hand_value()

                    #if the player wins then add double the bet amount
                    if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                        win_state = 'You Win!'
                        if not self.chips_added:
                            self.chips += self.bet_amount * 2
                            self.chips_added = True

                    #if tie then say push and refund the player
                    elif player_hand_value == dealer_hand_value:
                        win_state = 'Push'
                        if not self.chips_added:
                            self.chips += self.bet_amount
                            self.chips_added = True

                    #if lose then you get nothing
                    else:
                        win_state = 'You lose'
                        if self.bet_amount > self.chips:
                            self.bet_amount = self.chips
            pygame.display.flip()

    def print_community_cards(self, community_cards_hand, x, y, spacer, cards_to_show):
        # starts the hand at the fully left position
        i = x - (len(community_cards_hand) * community_cards_hand[0].image.get_width() / 2) - (spacer * len(community_cards_hand) // 2)
        for card in community_cards_hand:
            # if it is not the last card in the hand, draw
            if community_cards_hand.index(card) <= cards_to_show - 1:
                self.surface.blit(card.image, (i, y))
            # otherwise, draw the back of a card (hidden card)
            else:
                self.surface.blit(self.card_back, (i, y))
            # increments the card by the width of the card plus the spacer value
            i += card.image.get_width() + spacer

    def check_poker_hands(self, player_cards, community_cards):
        same_suits = 0
        same_suit_ranks = []
        return_value = 'High Card'
        cards_to_check = community_cards.copy()

        card_ranks = []

        #adds the river cards into a cards to check list
        for card in player_cards:
            cards_to_check.append(card)
        for card in cards_to_check:
            if isinstance(card.rank, str): card.rank = self.poker_card_values[card.rank]

        #sorts the list by rank
        cards_to_check.sort(key=lambda x: x.rank)

        # Creates a list of only card ranks for faster checking later
        for i in cards_to_check:
            card_ranks.append(i.rank)

        #for loop to check through all cards, this is a very inefficient function
        for i in cards_to_check:
            #flush
            for k in cards_to_check:
                if i.suit == k.suit:
                    same_suits += 1
                    same_suit_ranks.append(k.rank)
                    same_suit_ranks.sort()
                    if same_suits == 5:
                        if same_suit_ranks[0] + 4 == same_suit_ranks[4]:
                             return_value = 'Straight Flush'
                        else:
                            if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Flush']:
                                return_value = 'Flush'
                if cards_to_check.index(k) == 6:
                    same_suits = 0
                    same_suit_ranks = []

            #straight
            if i.rank + 1 in card_ranks and i.rank + 2 in card_ranks and i.rank + 3 in card_ranks and i.rank + 4 in card_ranks:
                if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Straight']:
                    return_value = 'Straight'

            #quads
            if cards_to_check.index(i) <= 3 and i.rank == cards_to_check[(cards_to_check.index(i) + 3)].rank:
                if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Four of a Kind']:
                    return_value = 'Four of a Kind'

            #trips and full house
            if cards_to_check.index(i) <= 4 and i.rank == cards_to_check[(cards_to_check.index(i) + 2)].rank:
                current_rank = i.rank
                for k in card_ranks:
                    if card_ranks.index(k) <= 5 and k == card_ranks[(card_ranks.index(k) + 1)] and k != current_rank:
                        if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Full House']:
                            return_value = 'Full House'
                            break
                else:
                    if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Three of a Kind']:
                        return_value = 'Three of a Kind'

            # pair and two pair
            if cards_to_check.index(i) <= 5 and i.rank == cards_to_check[(cards_to_check.index(i) + 1)].rank:
                current_rank = i.rank
                for k in card_ranks:
                    if card_ranks.index(k) <= 5 and k == card_ranks[(card_ranks.index(k) + 1)] and k != current_rank:
                        if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['Two Pair']:
                            return_value = 'Two Pair'
                            break
                else:
                    if self.poker_hand_rankings[return_value] < self.poker_hand_rankings['One Pair']:
                        return_value = 'One Pair'

        return return_value

    def poker_reset_game(self):
        self.community_cards = CommunityCards(self.deck)
        self.poker_player = PokerPlayer(self.deck, 0, 'Player')
        self.cpu_1.__init__(self.deck, 5, 'CPU1')
        self.cpu_2.__init__(self.deck, 0, 'CPU2')
        self.cpu_3.__init__(self.deck, 10, 'CPU3')
        for cpu in self.cpus:
            cpu.hand_value = self.check_poker_hands(cpu.hand, self.community_cards.cards)
        self.poker_player.hand_value = self.check_poker_hands(self.poker_player.hand, self.community_cards.cards)
        self.poker_player.bet = 0
        self.betting_round = 0
        self.cpus = [self.cpu_1, self.cpu_2, self.cpu_3]
        self.cpu_hands = [self.cpu_1.hand, self.cpu_2.hand, self.cpu_3.hand]
        self.poker_players = [self.poker_player, self.cpu_1, self.cpu_2, self.cpu_3]


    def cpu_play(self, cpu, chb):
        #determines the necessary bet to call
        btc = chb - cpu.bet
        random_num = random.random()
        if self.poker_hand_rankings[cpu.hand_value] < self.poker_hand_rankings[self.poker_player.hand_value]:
            #will fold 80% if the time its down
            if 0.1 < random_num < 0.8:
                return cpu.bet, False
            #will raise 10% of the time its down (bluff)
            elif random_num <= 0.1:
                cpu.bet += btc + 10
                return cpu.bet, True
            # otherwise it will call
            else:
                cpu.bet += btc
                return cpu.bet, True
        else:
            #will raise 30% of the time when its winning
            if random_num <= 0.3:
                cpu.bet += btc + 10
                return cpu.bet, True
            #will check 65% of the time
            elif 0.3 < random_num < 0.95:
                cpu.bet += btc
                return cpu.bet, True
            #will fold the rest of the time (to make it a little bit more fair)
            else:
                return cpu.bet, False

    #the cards argument is all the cards from every cpu hand
    def print_cpu_hands(self, showdown, cards):
        #won't print cards if there aren't any to print
        if cards == 0: cards = (None, None, None)
        #calculates the space that should be in between each card
        spacer = self.screen_width / 200
        card_width = self.card_back.get_width()
        #one for each hand, stored as (cards (the index is which cpu it is), (x, y))
        cpu_hands = ((cards[0], (self.screen_width * 0.25, self.screen_height * 0.4)), (cards[1], (self.screen_width * 0.5, self.screen_height * 0.15)), (cards[2], (self.screen_width * 0.75, self.screen_height * 0.4)))
        for hand in cpu_hands:
            #hand[1][0] is the x pos, as it refers to the first element (x) of the second element (the tuple (x,y) of the element of cpu_hands (the cpu hand it is currently on0
            i = hand[1][0] - (card_width + spacer)
            for x in range(2):
                # draws the card
                #cards will always be defined if showdown is true, so you will always be able to index this (don't worry about the error)
                if showdown: self.surface.blit(hand[0][x].image, (i, hand[1][1]))
                #else print the backs of the cards
                else: self.surface.blit(self.card_back, (i, hand[1][1]))
                # increments the card by the width of the card plus the spacer value
                i += card_width + spacer

    def poker_check_win(self):
        winners = []
        winning_hand_value = max(self.poker_hand_rankings[self.poker_player.hand_value], self.poker_hand_rankings[self.cpu_1.hand_value], self.poker_hand_rankings[self.cpu_2.hand_value], self.poker_hand_rankings[self.cpu_3.hand_value])
        for cpu in self.cpus:
            if self.poker_hand_rankings[cpu.hand_value] == winning_hand_value and cpu.playing:
                print(f'{cpu.name} wins')
                winners.append(cpu.name)
        if self.poker_hand_rankings[self.poker_player.hand_value] == winning_hand_value:
            print('player wins')
            winners.append('player')
        return winners

    def print_winners(self, winners):
        for index, winner in enumerate(winners):
            self.fonts[100].render_to(self.surface, (self.screen_width / 3 + index * self.screen_width / 10, self.screen_height / 2.7), f'{winner}',(255, 255, 255))




    def play_poker(self):
        #initializes the center cards
        self.community_cards = CommunityCards(self.deck)
        #initializes the player
        self.poker_player = PokerPlayer(self.deck, 0, 'Player')
        #immediately checks the value of the player hand
        self.poker_player.hand_value = self.check_poker_hands(self.poker_player.hand, self.community_cards.cards)
        #initializes the 3 cpus - cpu_1 is betting the small blind and cpu_3 is betting the big blind always
        self.cpu_1 = PokerCPU(self.deck, 5, 'CPU1')
        self.cpu_2 = PokerCPU(self.deck, 10, 'CPU2')
        self.cpu_3 = PokerCPU(self.deck, 0, 'CPU3')
        #a list of the cpus (so you can iterate through each
        self.cpus = [self.cpu_1, self.cpu_2, self.cpu_3]
        #a list of the cpus hands (useful for printing them)
        #checks the value of each of the cpus hands
        for cpu in self.cpus:
            cpu.hand_value = self.check_poker_hands(cpu.hand, self.community_cards.cards)
        #sets your initial bet to 0 and the betting round to the 1st (pre-flop)
        self.poker_player.bet = 0
        self.betting_round = 0
        #initializes the buttons
        fold_button = Button(self.screen_width * 0.61, self.screen_height / 2 + self.screen_height / 5, self.screen_width / 8, self.screen_height / 10, (255, 0, 0), 'Fold', 'CASINO', 40, (0, 0, 0))
        call_button = Button(self.screen_width * 0.27, self.screen_height / 2 + self.screen_height / 5, self.screen_width / 8, self.screen_height / 10, (255, 0, 0), f'Call ({self.poker_player.bet})', 'CASINO', 40, (0, 0, 0))
        raise_button = Button(self.screen_width * 0.27, self.screen_height / 2 + self.screen_height / 3, self.screen_width / 8, self.screen_height / 10, (255, 0, 0), f'Raise ({self.poker_player.bet})', 'CASINO', 40, (0, 0, 0))
        play_again_button = Button(self.screen_width * 0.7, self.screen_height / 6, self.screen_width / 5, self.screen_height / 5, (255, 0, 0), 'Play Again', 'CASINO', 40, (0, 0, 0))
        back_button = Button(self.screen_width / 20, self.screen_width / 40, self.screen_height / 10, self.screen_width / 20, (14, 237, 70), 'X', "GD", 40, (245, 200, 76))
        play_again_button.press = False
        poker_running = True

        win_checked = False

        self.cpus = [self.cpu_1, self.cpu_2, self.cpu_3]
        self.cpu_hands = [self.cpu_1.hand, self.cpu_2.hand, self.cpu_3.hand]
        self.poker_players = [self.cpu_1, self.cpu_2, self.cpu_3, self.poker_player]

        self.poker_player.played = False

        current_player_number = 0

        while poker_running:
            bets = [self.poker_player.bet, self.cpu_1.bet, self.cpu_2.bet, self.cpu_3.bet]
            pot = sum(bets)
            active_bets = [player.bet for player in self.poker_players if player.playing]
            current_highest_bet = max(bets)
            bet_to_call = current_highest_bet - self.poker_player.bet
            call_button.text = f'Call ({bet_to_call})'
            raise_button.text = f'Raise ({bet_to_call + 10})'
            current_player = self.poker_players[current_player_number]
            if isinstance(current_player, PokerCPU):
                if current_player.bet < current_highest_bet and current_player.playing:
                    current_player.bet, current_player.playing = self.cpu_play(current_player, current_highest_bet)
                current_player_number += 1
            if len(set(active_bets)) == 1 and self.poker_player.played:
                self.poker_player.played = False
                self.betting_round += 1
                print(self.betting_round)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.chips, None
                if fold_button.check_button_click(event):
                    self.poker_player.playing = False
                    current_player_number = 0
                    self.betting_round = 4
                if call_button.check_button_click(event):
                    self.poker_player.bet += bet_to_call
                    current_player_number = 0
                    self.poker_player.played = True
                if raise_button.check_button_click(event):
                    self.poker_player.bet += bet_to_call + 10
                    current_player_number = 0
                    self.poker_player.played = True
                if play_again_button.check_button_click(event):
                    self.poker_reset_game()
                    current_player_number = 0
                    win_checked = False
                    call_button.press = True
                    raise_button.press = True
                    fold_button.press = True
                    play_again_button.press = False
                    back_button.press = False
                if back_button.check_button_click(event):
                    return self.chips, True


            self.surface.fill((16, 82, 9))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.47, self.screen_height * 0.83), f'Your Bet: {self.poker_player.bet}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.47, self.screen_height * 0.86), f'Your Chips: {self.chips}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.47, self.screen_height * 0.89), f'Your Hand: {self.poker_player.hand_value}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width / 15, self.screen_height / 3), f'Pot: {pot}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.2, self.screen_height * 0.59),f'Bet: {self.cpu_1.bet}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.45, self.screen_height * 0.32),f'Bet: {self.cpu_2.bet}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (self.screen_width * 0.76, self.screen_height * 0.59),f'Bet: {self.cpu_3.bet}', (255, 255, 255))
            fold_button.draw_button(self.surface)
            call_button.draw_button(self.surface)
            raise_button.draw_button(self.surface)
            if self.betting_round == 0:
                self.print_community_cards(self.community_cards.cards, self.screen_width / 2, self.screen_height / 2.5, 5, 0)
                self.print_cpu_hands(0, 0)
            elif self.betting_round == 1:
                self.print_community_cards(self.community_cards.cards, self.screen_width / 2, self.screen_height / 2.5, 5, 3)
                self.print_cpu_hands(0, 0)
            elif self.betting_round == 2:
                self.print_community_cards(self.community_cards.cards, self.screen_width / 2, self.screen_height / 2.5, 5, 4)
                self.print_cpu_hands(0, 0)
            elif self.betting_round == 3:
                self.print_community_cards(self.community_cards.cards, self.screen_width / 2, self.screen_height / 2.5, 5, 5)
                self.print_cpu_hands(1, self.cpu_hands)
            elif self.betting_round == 4:
                self.print_community_cards(self.community_cards.cards, self.screen_width / 2, self.screen_height / 2.5, 5, 5)
                play_again_button.press = True
                back_button.press = True
                call_button.press = False
                raise_button.press = False
                fold_button.press = False
                if not win_checked:
                    winners = self.poker_check_win()
                    win_checked = True
                self.print_winners(winners)
                play_again_button.draw_button(self.surface)
                back_button.draw_button(self.surface)
                self.print_cpu_hands(1, self.cpu_hands)
            else: self.betting_round = 0
            self.print_player_hand(self.poker_player.hand, self.screen_width / 2, self.screen_height * 0.65, 5)
            self.fonts[18].render_to(self.surface, (10, 10), f'CPU 1 - hand: {self.cpu_1.hand_value}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (20, 40), f'bet: {self.cpu_1.bet}', (255, 255, 255))

            self.fonts[18].render_to(self.surface, (10, 70), f'CPU 2 - hand: {self.cpu_2.hand_value}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (20, 100), f'bet: {self.cpu_2.bet}', (255, 255, 255))

            self.fonts[18].render_to(self.surface, (10, 130), f'CPU 3 - hand: {self.cpu_3.hand_value}', (255, 255, 255))
            self.fonts[18].render_to(self.surface, (20, 160), f'bet: {self.cpu_3.bet}', (255, 255, 255))

            pygame.display.flip()