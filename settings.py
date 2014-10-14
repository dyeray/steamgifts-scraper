# -*- coding: utf-8 -*-

import json

SETTINGS_PATH = 'settings.cfg'


class Settings:

    def __init__(self):
        self._json_settings = json.load(open(SETTINGS_PATH))

    def save(self):
        json.dump(self._json_settings, open(SETTINGS_PATH, "w"))

    def get_username(self):
        return self._json_settings['username']

    def get_password(self):
        return self._json_settings['password']

    def get_games(self):
        return self._json_settings['games']

    def add_game(self, title, priority):
        self._json_settings['games'][title] = priority
