import pygame
from game_classes import Button

class UpgradeScreenManager:
    def __init__(self, screen, screen_width, screen_height, game_manager):
        self.surface = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_manager = game_manager
        self.in_upgrade_screen = True
        chip_mult_button = Button(self.screen_width * 0.2, self.screen_height / 2 + self.screen_height / 6, self.screen_width / 8, self.screen_height / 5, (255, 0, 0), '+1 Chip Mult (100)', 'GD', 40, (0, 0, 0))
        while self.in_upgrade_screen:
            self.surface.fill((0,0,255))
            chip_mult_button.draw_button(self.surface)
