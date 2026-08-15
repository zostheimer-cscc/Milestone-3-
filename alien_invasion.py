"""
Program Name: Alien Invasion Main

Author: Zachary Ostheimer

Purpose: This program runs the main game loop for Alien Invasion

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from hud import HUD
from button import Button


class AlienInvasion:
    #manages the game setup, the main loop, states, and all events

    def __init__(self) -> None:
        #start pygame and build every part of the game
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h)
        )

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.game_stats = GameStats(self)
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.hud = HUD(self)
        self.play_button = Button(self, 'Play')

        self.game_active = False
        #the game waits on the Play button before starting

    def run_game(self) -> None:
        # Game loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self) -> None:
        #check bullet hits, level clears, and the two loss conditions
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.hud.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._advance_level()
        #the fleet was wiped out, move up a level

        if self.alien_fleet.check_ship_collision(self.ship):
            self._check_game_status()
        #an alien touched the ship

        if self.alien_fleet.check_fleet_left():
            self._check_game_status()
        #an alien slipped past the left edge

    def _check_game_status(self) -> None:
        #lose a life and reset, or end the game if out of lives
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        #show the cursor again when the game ends

    def _reset_level(self) -> None:
        #clear bullets and rebuild the fleet for another life
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.fleet_direction = self.settings.fleet_direction
        self.alien_fleet.create_fleet()

    def _advance_level(self) -> None:
        #speed the game up and start the next level
        self._reset_level()
        self.settings.increase_difficulty()
        self.game_stats.update_level()
        self.hud.update_level()

    def _start_game(self) -> None:
        #reset everything and begin a fresh game
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.hud.update_scores()
        self.hud.update_level()
        self.game_active = True

        self._reset_level()
        pygame.mouse.set_visible(False)
        #hide the cursor while the game is active

    def _update_screen(self) -> None:
        #draw the background, ship, fleet, HUD, and Play button
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.hud.draw()

        if not self.game_active:
            self.play_button.draw()

        pygame.display.flip()

    def _check_events(self) -> None:
        #watch for quit, mouse clicks, and key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicked(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_button_clicked(self, mouse_pos: tuple) -> None:
        #start the game if the Play button was clicked while idle
        if not self.game_active and self.play_button.check_clicked(mouse_pos):
            self._start_game()

    def _check_keyup_events(self, event) -> None:
        #stop moving when a movement key is released
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _check_keydown_events(self, event) -> None:
        #move, fire, or quit when a key is pressed
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and self.game_active:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
