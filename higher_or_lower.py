import random
import pygame
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
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync=1)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        self.image = pygame.image.load(f"Assets/Cards/{self.rank}of{self.suit}.png")
        self.image = pygame.transform.scale(self.image, (70, 109))

    def __repr__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    def __init__(self):
        suits = ("Hearts", "Diamonds", "Spades", "Crosses")
        ranks = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

        self.shuffle()

    def deal(self):
        # Reshuffle when the deck runs out
        if len(self.cards) == 0:
            self.__init__()

        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

# Ace is highest
card_values = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'10': 10,'Jack': 11,'Queen': 12,'King': 13,'Ace': 14}


def get_card_value(card):
    return card_values[card.rank]

my_deck = Deck()

# Starting chips
chips = 100

# Starting card
current_card = my_deck.deal()
next_card = None

# Game state
guess = None
round_over = False
round_scored = False
result_text = ""
result_color = (255, 255, 255)

running = True

higher_button = Button(SCREENWIDTH * 0.15,SCREENHEIGHT * 0.65,SCREENWIDTH / 4,SCREENHEIGHT / 6,(255, 0, 0),('Higher', 'Assets/casino.ttf', 32, (0, 0, 0)))

lower_button = Button(SCREENWIDTH * 0.6,SCREENHEIGHT * 0.65,SCREENWIDTH / 4,SCREENHEIGHT / 6,(255, 0, 0),('Lower', 'Assets/casino.ttf', 32, (0, 0, 0)))

play_again_button = Button(SCREENWIDTH * 0.375, SCREENHEIGHT * 0.78, SCREENWIDTH / 4, SCREENHEIGHT / 6,(255, 0, 0),('Play Again', 'Assets/casino.ttf', 32, (0, 0, 0)))

# Only show Play Again after a round ends
play_again_button.press = False

while running:
    screen.fill((16, 82, 9))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Guess Higher
        if not round_over and higher_button.check_button_click(event):
            guess = "higher"
            next_card = my_deck.deal()
            round_over = True
        # Guess Lower
        if not round_over and lower_button.check_button_click(event):
            guess = "lower"
            next_card = my_deck.deal()
            round_over = True
        # Play another round
        if round_over and play_again_button.check_button_click(event):
            current_card = next_card
            next_card = None
            guess = None
            round_over = False
            round_scored = False
            result_text = ""
            play_again_button.press = False
    CASINO_FONTS[18].render_to(screen,(50, 30),f"Your Chips: {chips}",(255, 255, 255))
    CASINO_FONTS[32].render_to(screen,(SCREENWIDTH / 2 - 100, 65),"Current Card",(255, 255, 255))
    screen.blit(current_card.image, (SCREENWIDTH / 2 - 35, 110))
    if not round_over:
        CASINO_FONTS[24].render_to(screen,  (SCREENWIDTH / 2 - 200, 245),"Will the next card be higher or lower?",(255, 255, 255))
        higher_button.draw_button(screen)
        higher_button.render_text(screen)
        lower_button.draw_button(screen)
        lower_button.render_text(screen)
    else:

        # Calculate and award chips only once per round
        if not round_scored:
            current_value = get_card_value(current_card)
            next_value = get_card_value(next_card)
            if next_value == current_value:
                result_text = "Bro run it back."
                result_color = (255, 255, 0)
            elif (guess == "higher" and next_value > current_value) or (guess == "lower" and next_value < current_value):
                result_text = "Correct!"
                result_color = (0, 255, 0)
                chips += 50
            else:
                result_text = "Wrong!"
                result_color = (255, 80, 80)
                chips -= 50

            round_scored = True
            play_again_button.press = True

        # Show the next card
        CASINO_FONTS[24].render_to(screen,(SCREENWIDTH / 2 - 65, 245),"Next Card",(255, 255, 255))

        screen.blit(next_card.image,(SCREENWIDTH / 2 - 35, 285))

        # Display result
        result_rect = CASINO_FONTS[24].get_rect(result_text)

        CASINO_FONTS[24].render_to(screen,((SCREENWIDTH - result_rect.width) / 2, 410), result_text, result_color)

        # Play Again button
        play_again_button.draw_button(screen)
        play_again_button.render_text(screen)

    pygame.display.flip()

pygame.quit()
