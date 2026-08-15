"""
Program Name: Alien Invasion HUD

Author: Zachary Ostheimer

Purpose: This module draws the score, high score, level, and lives on screen

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import pygame.font
from pygame.sprite import Group
from ship import Ship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    #draws the score, high score, level, and remaining lives

    def __init__(self, game: 'AlienInvasion') -> None:
        #set up the HUD fonts, padding, and first render
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(
            self.settings.font_file, self.settings.HUD_font_size
        )
        self.padding = 20

        self.update_scores()
        self._setup_life_image()
        self.update_level()

    def _setup_life_image(self) -> None:
        #load and scale the small ship icon used for lives
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(
            self.life_image, (self.settings.ship_w, self.settings.ship_h)
        )
        self.life_rect = self.life_image.get_rect()

    def update_scores(self) -> None:
        #re-render all three score readouts
        self._update_score()
        self._update_max_score()
        self._update_high_score()

    def _update_score(self) -> None:
        #render the current score at the top right
        score_str = f'Score: {self.game_stats.score:,.0f}'
        self.score_image = self.font.render(
            score_str, True, self.settings.font_color, None
        )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.padding

    def _update_max_score(self) -> None:
        #render the session high score at the top center
        max_score_str = f'High: {self.game_stats.max_score:,.0f}'
        self.max_score_image = self.font.render(
            max_score_str, True, self.settings.font_color, None
        )
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def _update_high_score(self) -> None:
        #render the saved all time high score below the session high
        high_score_str = f'Best: {self.game_stats.high_score:,.0f}'
        self.high_score_image = self.font.render(
            high_score_str, True, self.settings.font_color, None
        )
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (
            self.boundaries.centerx, self.max_score_rect.bottom + self.padding
        )

    def update_level(self) -> None:
        #render the current level at the top left
        level_str = f'Level: {self.game_stats.level:,.0f}'
        self.level_image = self.font.render(
            level_str, True, self.settings.font_color, None
        )
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.padding

    def _draw_lives(self) -> None:
        #draw one ship icon for each life the player has left
        current_x = self.padding
        current_y = self.level_rect.bottom + self.padding
        for life in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self) -> None:
        #draw every part of the HUD onto the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()
