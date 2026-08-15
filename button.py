"""
Program Name: Alien Invasion Button

Author: Zachary Ostheimer

Purpose: This module makes the Play button that starts the game

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    #a clickable Play button shown before the game starts

    def __init__(self, game: 'AlienInvasion', msg: str) -> None:
        #set up the button size, position, and label
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.settings = game.settings

        self.font = pygame.font.Font(
            self.settings.font_file, self.settings.button_font_size
        )

        self.width = 300
        self.height = 100
        self.button_color = self.settings.button_color

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.boundaries.center
        #place the button in the middle of the screen

        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        #render the button text and center it on the button
        self.msg_image = self.font.render(
            msg, True, self.settings.font_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self) -> None:
        #draw the button box and its label
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos: tuple) -> bool:
        #return True if the click landed inside the button
        return self.rect.collidepoint(mouse_pos)
