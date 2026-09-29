#this is the file to create the gambling
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__:


class Deck:
    def __init__(self):
        suits = ("hearts", "diamonds", "spades", "clubs")
        ranks = ('A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}



my_deck = Deck()