"""
Program Name: Alien Invasion Settings

Author: Zachary Ostheimer

Purpose: This module stores all the static and dynamic settings for the game

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

from pathlib import Path

#gets the folder this file is in so assets load from anywhere
BASE_PATH = Path(__file__).parent


class Settings:
    #holds every setting the game needs in one place

    def __init__(self) -> None:
        #set up the static settings that never change during play
        self.name: str = 'Alien Invasion'
        self.screen_w: int = 1200
        self.screen_h: int = 800
        self.FPS: int = 60
        self.bg_file = BASE_PATH / 'Assets' / 'images' / 'Starbasesnow.png'

        self.ship_file = BASE_PATH / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w: int = 60
        self.ship_h: int = 40
        self.starting_ship_count: int = 3
        #the player starts each game with 3 lives

        self.bullet_file = BASE_PATH / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = BASE_PATH / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = BASE_PATH / 'Assets' / 'sound' / 'impactSound.mp3'
        self.bullet_w: int = 80
        self.bullet_h: int = 25
        self.bullet_amount: int = 5

        self.alien_file = BASE_PATH / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w: int = 60
        self.alien_h: int = 60
        self.fleet_speed: int = 1
        self.fleet_direction: int = 1
        #1 moves the fleet down, -1 moves it up
        self.fleet_step_left: int = 60
        self.fleet_cols: int = 4

        self.scores_file = BASE_PATH / 'Assets' / 'file' / 'scores.json'
        self.font_file = BASE_PATH / 'Assets' / 'Fonts\Silkscreen' / 'Silkscreen-Regular.ttf'
        self.HUD_font_size: int = 40
        self.button_font_size: int = 48
        self.font_color = (255, 255, 255)
        self.button_color = (0, 135, 50)

        #how much speeds go up each level
        self.speedup_scale: float = 1.1
        self.score_scale: float = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        #set up the settings that reset at the start of each new game
        self.ship_speed: float = 5.0
        self.bullet_speed: float = 7.0
        self.fleet_speed: float = 2.0
        self.alien_points: int = 50

    def increase_difficulty(self) -> None:
        #speed everything up and raise the points when a level is cleared
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.fleet_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
