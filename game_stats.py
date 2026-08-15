"""
Program Name: Alien Invasion Game Stats

Author: Zachary Ostheimer

Purpose: This module tracks score, high score, level, and lives

Starter Code: Based on the in class Alien Invasion tutorial

Date: 08/14/2026
"""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats:
    #keeps track of the score, high score, level, and lives

    def __init__(self, game: 'AlienInvasion') -> None:
        #set up the stats and load the saved high score
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        #read the high score from the save file if it exists
        self.path = self.settings.scores_file
        self.high_score = 0
        if self.path.exists() and self.path.stat().st_size > 0:
            try:
                contents = self.path.read_text()
                scores = json.loads(contents)
                self.high_score = scores.get('high_score', 0)
            except json.JSONDecodeError:
                #a blank or corrupt file starts the high score fresh
                self.save_scores()
        else:
            self.save_scores()

    def save_scores(self) -> None:
        #write the current high score to the save file
        scores = {'high_score': self.high_score}
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')

    def reset_stats(self) -> None:
        #reset the stats that change during a single game
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions: dict) -> None:
        #update the score and high score after a hit
        self._update_score(collisions)
        self._update_max_score()
        self._update_high_score()

    def _update_max_score(self) -> None:
        #track the highest score of the current session
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_high_score(self) -> None:
        #save a new high score when the score passes it
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_scores()

    def _update_score(self, collisions: dict) -> None:
        #add points for every alien destroyed in this hit
        for aliens in collisions.values():
            self.score += self.settings.alien_points * len(aliens)

    def update_level(self) -> None:
        #move up one level
        self.level += 1
