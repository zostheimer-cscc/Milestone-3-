"""
Program Name: Alien Invasion Alien

Author: Zachary Ostheimer

Purpose: This module controls a single alien in the fleet

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet


class Alien(Sprite):
    #a single alien that marches up and down and steps left

    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        #set up the alien image and its starting position
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.alien_w, self.settings.alien_h)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        #track position as floats for smooth movement

    def update(self) -> None:
        #move the alien vertically based on the fleet direction
        temp_speed = self.settings.fleet_speed
        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.y = self.y

    def check_edges(self) -> bool:
        #return True if the alien hit the top or bottom edge
        return (self.rect.bottom >= self.boundaries.bottom or
                self.rect.top <= self.boundaries.top)

    def draw_alien(self) -> None:
        #draw the alien on the screen
        self.screen.blit(self.image, self.rect)
