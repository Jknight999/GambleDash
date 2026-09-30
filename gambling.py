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
supported_games = {'blackjack'}

#dictionary mapping card ranks to card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, "10": 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
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

#prints
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

#checks for which of the games they would like to play - obviously the only option rn is blackjack
print('What casino game would you like to play?\nCurrently supported games: ', end='')
for game in supported_games:
    print(game, end=' ')
current_game = input('').lower()
while current_game.lower() not in supported_games:
    current_game = input('That game is currently not supported. Please enter the name of a supported game: ').lower()

#actual 'game loop'
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