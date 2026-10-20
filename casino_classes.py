import pygame
import random

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

class BlackjackHand:
    def __init__(self, deck):
        self.cards = []
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
            'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
        }
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