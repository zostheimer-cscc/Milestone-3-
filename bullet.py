"""
Program Name: Alien Invasion Bullet

Author: Zachary Ostheimer

Purpose: This module controls a single laser bullet that flies right

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/13/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    #a single laser that spawns at the ship and travels right

    def __init__(self, game: 'AlienInvasion') -> None:
        #set up the bullet image, rotation, and starting position
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.bullet_w, self.settings.bullet_h)
        )
        self.image = pygame.transform.rotate(self.image, -90)
        #rotate so the laser points right

        self.rect = self.image.get_rect()
        self.rect.midleft = game.ship.rect.midright
        #start the bullet at the front of the ship

        self.x = float(self.rect.x)
        #track x as a float for smooth movement

    def update(self) -> None:
        #move the bullet to the right each frame
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self) -> None:
        #draw the bullet on the screen
        self.screen.blit(self.image, self.rect)
