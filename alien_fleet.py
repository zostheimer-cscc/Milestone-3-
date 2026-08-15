"""
Program Name: Alien Invasion Alien Fleet

Author: Zachary Ostheimer

Purpose: This module builds and moves the whole alien fleet

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:
    #creates the fleet and moves it as one group

    def __init__(self, game: 'AlienInvasion') -> None:
        #set up the fleet group and build the starting fleet
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction

        self.create_fleet()

    def create_fleet(self) -> None:
        #build the block of aliens on the right side of the screen
        alien_h = self.settings.alien_h
        alien_w = self.settings.alien_w
        screen_h = self.settings.screen_h
        screen_w = self.settings.screen_w

        fleet_h = self.calculate_fleet_size(alien_h, screen_h)
        cols = self.settings.fleet_cols

        fleet_vertical_space = fleet_h * alien_h
        y_offset = int((screen_h - fleet_vertical_space) // 2)
        #center the fleet vertically on the screen

        for row in range(fleet_h):
            for col in range(cols):
                current_y = alien_h * row + y_offset
                current_x = screen_w - alien_w * (col + 1) - alien_w
                #stack columns inward from the right edge
                self._create_alien(current_x, current_y)

    def calculate_fleet_size(self, alien_h: int, screen_h: int) -> int:
        #figure out how many aliens tall the fleet can be
        fleet_h = (screen_h // alien_h)

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return fleet_h

    def _create_alien(self, current_x: int, current_y: int) -> None:
        #make one alien and add it to the fleet group
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self) -> None:
        #reverse direction and step left if any alien hit an edge
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._reverse_and_step_left()
                break

    def _reverse_and_step_left(self) -> None:
        #flip the vertical direction and move the whole fleet left
        alien: Alien
        for alien in self.fleet:
            alien.x -= self.settings.fleet_step_left
            alien.rect.x = alien.x
        self.fleet_direction *= -1

    def update_fleet(self) -> None:
        #check edges then move every alien in the fleet
        self._check_fleet_edges()
        self.fleet.update()

    def check_collisions(self, other_group: pygame.sprite.Group) -> dict:
        #return a dict of bullets that hit aliens, removing both
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_left(self) -> bool:
        #return True if any alien reached the left edge behind the ship
        alien: Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False

    def check_ship_collision(self, ship) -> bool:
        #return True if any alien collided with the ship
        return pygame.sprite.spritecollideany(ship, self.fleet) is not None

    def check_destroyed_status(self) -> bool:
        #return True if every alien in the fleet is gone
        return not self.fleet

    def draw(self) -> None:
        #draw every alien in the fleet
        alien: Alien
        for alien in self.fleet:
            alien.draw_alien()
