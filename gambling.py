import random

#this is the file to create the gambling
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    #basically just represents it as a string (for printing purposes)
    def __repr__(self):
        return f'{self.rank} of {self.suit}'
class Deck:
    def __init__(self):
        suits = ("hearts", "diamonds", "spades", "clubs")
        ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
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

#dictionary mapping card ranks to card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def calculate_hand(hand):
    current_values = [card_values[s.rank] for s in hand]
    current_values.sort()
    hand_value = 0
    for value in current_values:
        if value != 11:
            hand_value += value
        elif hand_value < 11:
            hand_value += value
        else: hand_value += 1
    return hand_value

my_deck = Deck()
my_deck.shuffle()

chips = 100
def print_player_hand():
    global player_hand
    print(f"\nYour hand: ", end='')
    for i in range(len(player_hand)):
        print(player_hand[i], end=' ')
    print(f"\nHand value: {calculate_hand(player_hand)}\n")

def print_dealer_hand():
    global dealer_hand
    print(f"Dealer Hand: {dealer_hand[0]}, unknown\n")

def blackjack_start_hand():
    hand = []
    for _ in range(2):
        hand.append(my_deck.deal())
    return hand

while chips > 0:
    print(f"You have {chips} chips.")
    bet = input("How many chips would you like to bet? ")
    while not (bet.isdigit() and 0 < int(bet) <= chips):
        bet = input("Invalid Input. How many chips would you like to bet? ")
    bet = int(bet)
    player_hand = blackjack_start_hand()
    print_player_hand()
    player_playing = True
    dealer_hand = blackjack_start_hand()
    dealer_hand_value = calculate_hand(dealer_hand)
    print_dealer_hand()
    dealer_playing = True
    while player_playing:
        player_action = input('What would you like to do (hit, stand, double)? ')
        while player_action not in blackjack_possible_actions:
            player_action = input('Invalid Action. What would you like to do (hit, stand, double)? ')
        if player_action == 'hit':
            player_hand.append(my_deck.deal())
            print_player_hand()
        elif player_action == 'stand':
            player_playing = False
        elif player_action == 'double':
            bet *= 2
            player_hand.append(my_deck.deal())
            print_player_hand()
            player_playing = False
        player_hand_value = calculate_hand(player_hand)
        if player_hand_value > 21:
            print("You busted.")
            dealer_playing = False
            break
    player_hand_value = calculate_hand(player_hand)
    while dealer_playing:
        dealer_hand_value = calculate_hand(dealer_hand)
        if dealer_hand_value <= 16:
            dealer_hand.append(my_deck.deal())
        elif dealer_hand_value == 17 and 'A' in dealer_hand:
            dealer_hand.append(my_deck.deal())
        else:
            dealer_playing = False
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