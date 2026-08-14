"""
Program Name: Alien Invasion Ship

Author: Zachary Ostheimer

Purpose: This module controls the player ship on the left edge

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/13/2026
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship:
    #the player ship that sits on the left and moves up and down

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        #set up the ship image, starting position, and arsenal
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.ship_w, self.settings.ship_h)
        )
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self.rect.midleft = self.boundaries.midleft
        #start the ship centered on the left edge

        self.moving_up = False
        self.moving_down = False
        self.y = float(self.rect.y)
        #track y as a float for smooth movement

        self.arsenal = arsenal

    def update(self) -> None:
        #move the ship and update its bullets each frame
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        #move the ship up or down within the screen edges
        temp_speed = self.settings.ship_speed

        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed

        self.rect.y = self.y

    def draw(self) -> None:
        #draw the ship and its bullets on the screen
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self) -> bool:
        #fire a bullet from the ship, return True if it fired
        return self.arsenal.fire_bullet()
