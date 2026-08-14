"""
Program Name: Alien Invasion Arsenal

Author: Zachary Ostheimer

Purpose: This module manages the group of bullets the ship fires

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/13/2026
"""

import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Arsenal:
    #manages all the bullets currently on screen

    def __init__(self, game: 'AlienInvasion') -> None:
        #set up the bullet group
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        #move all bullets and clear the ones that leave the screen
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        #remove bullets once they pass the right edge
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.settings.screen_w:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        #draw every bullet in the arsenal
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self) -> bool:
        #add a new bullet if under the limit, return True if fired
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
