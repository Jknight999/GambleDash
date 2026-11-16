#imports
import pygame
import random

class Card:
    def __init__(self, suit, rank):
        #basic inits
        self.suit = suit
        self.rank = rank
        screenwidth = pygame.display.get_desktop_sizes()[0][0]
        self.image = pygame.image.load(f"Assets/Cards/{self.rank}of{self.suit}.png")
        self.image = pygame.transform.scale(self.image, (352 / (screenwidth / 400), 544 / (screenwidth / 400)))

    #basically just represents it as a string (for printing purposes)
    #returns the suit and rank of a card
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

class BlackjackHand:
    def __init__(self, deck):
        self.cards = []
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
        }
        #gives the player 2 cards to start
        for _ in range(2):
            self.cards.append(deck.deal())

    def get_hand_value(self):
        # more list comp -- just translates the cards into their numerical values using the dict
        current_values = [self.card_values[s.rank] for s in self.cards]
        # so that we can take care of aces last
        current_values.sort()
        hand_value = 0
        # iterates through each value
        for value in current_values:
            # everything except for aces
            if value != 11:
                hand_value += value
            # just checks if adding and ace would make the hand bust
            elif hand_value < 11:
                hand_value += value
            else:
                hand_value += 1
        # returns the calculated value -- so CATCH IT
        return hand_value

    def deal_card(self, deck):
        self.cards.append(deck.deal())

class PokerHand:
    def __init__(self, deck):
        self.cards = []
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        #gives 2 player cards
        for _ in range(2):
            self.cards.append(deck.deal())

class CommunityCards:
    def __init__(self, deck):
        self.cards = []
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        #gives 5 river cards
        for _ in range(5):
            self.cards.append(deck.deal())

class PokerCPU:
    def __init__(self, deck, central_cards):
        self.hand = [deck.deal(), deck.deal()]
        self.playing = True
        self.bet = 0
        self.poker_card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        self.hand_value = self.calculate_hand_value(self.hand, central_cards)

    def calculate_hand_value(self, player_cards, community_cards,):
        same_suits = 0
        return_value = 0
        cards_to_check = player_cards.copy()

        # adds the river cards into a cards to check list
        for card in community_cards:
            cards_to_check.append(card)
        for card in cards_to_check:
            if isinstance(card.rank, str): card.rank = self.poker_card_values[card.rank]

        # sorts the list by rank
        cards_to_check.sort(key=lambda x: x.rank)

        # for loop to check through all cases
        for i in range(len(cards_to_check) - 1):
            # flush
            for k in cards_to_check:
                if cards_to_check[i].suit == k.suit:
                    same_suits += 1
                    if same_suits == 5:
                        return_value += 12
                if cards_to_check.index(k) == 6:
                    same_suits = 0

            # straight
            if i <= 2 and cards_to_check[i].rank - 4 == cards_to_check[i - 4].rank:
                return_value += 10

            # pairs, trips, quads
            if cards_to_check[i].rank == cards_to_check[i + 1].rank:
                if i < 5 and cards_to_check[i].rank == cards_to_check[i + 2].rank:
                    if i < 4 and cards_to_check[i].rank == cards_to_check[i + 3].rank:
                        return_value = 4
                        return 'four_of_a_kind'
                    else:
                        return_value += 5
                else:
                    return_value += 1

        # calculates what to return by giving each outcome a return value
        if return_value == 22:
            return 'straight_flush'
        elif return_value == 12 or return_value == 13:
            return 'flush'
        elif return_value == 10 or return_value == 11:
            return 'straight'
        elif return_value == 6 or return_value == 7:
            return 'full_house'
        elif return_value == 5:
            return 'three_of_a_kind'
        elif return_value == 2:
            return 'two_pair'
        elif return_value == 1:
            return 'pair'
        else:
            return 'high_card'