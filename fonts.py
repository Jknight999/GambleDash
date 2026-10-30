import pygame.freetype

pygame.freetype.init()

GD_FONTS = {
    14: pygame.freetype.Font('Assets/pusab.otf', 14),
    18: pygame.freetype.Font('Assets/pusab.otf', 18),
    24: pygame.freetype.Font('Assets/pusab.otf', 24),
    32: pygame.freetype.Font('Assets/pusab.otf', 32),
    40: pygame.freetype.Font('Assets/pusab.otf', 40),
    50: pygame.freetype.Font('Assets/pusab.otf', 50),
    100: pygame.freetype.Font('Assets/pusab.otf', 100)
}

CASINO_FONTS = {
    14: pygame.freetype.Font('Assets/casino.ttf', 14),
    18: pygame.freetype.Font('Assets/casino.ttf', 18),
    24: pygame.freetype.Font('Assets/casino.ttf', 24),
    32: pygame.freetype.Font('Assets/casino.ttf', 32),
    40: pygame.freetype.Font('Assets/casino.ttf', 40),
    50: pygame.freetype.Font('Assets/casino.ttf', 50),
    80: pygame.freetype.Font('Assets/casino.ttf', 80),
    100: pygame.freetype.Font('Assets/casino.ttf', 100)
}