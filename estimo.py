# -*- coding: utf-8 -*-
from selenium import webdriver
import json
import sys

SETTINGS_PATH = 'settings.cfg'


class Estimo:
    def __init__(self):
        self.drv = webdriver.Firefox()
        self.drv.implicitly_wait(10)
        self.base_url = "http://www.steamgifts.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.settings = self._load_settings()

    def run(self):
        self.estimo()
        self.close()

    def close(self):
        self.drv.quit()

    def login(self):
        self.drv.get(self.base_url + "/")
        self.drv.find_element_by_css_selector("img.login").click()
        self.drv.find_element_by_id("steamAccountName").clear()
        self.drv.find_element_by_id("steamAccountName").send_keys(self.settings['username'])
        self.drv.find_element_by_id("steamPassword").clear()
        self.drv.find_element_by_id("steamPassword").send_keys(self.settings['password'])
        self.drv.find_element_by_id("imageLogin").click()

    def _scan(self):
        self.drv.get(self.base_url + "/")
        return self.drv.find_elements_by_xpath(
            '//div[@class="ajax_gifts"]//div[@class="title"]//a')

    def _load_settings(self):
        return json.load(open(SETTINGS_PATH))

    def _save_settings(self):
        json.dump(self.settings, open(SETTINGS_PATH, "w"))

    def scan(self):
        games = self.settings["games"]
        new_games = {g.text for g in self._scan()}
        for ng in new_games:
            if ng not in games:
                decision = raw_input("New game found: '" + ng +
                                     "'. Do you want to automatically access its giveaways (y/n)?")
                if decision == 'y':
                    self.settings["games"][ng] = 1
                else:
                    self.settings["games"][ng] = 0
        self._save_settings()

    def estimo(self):
        self.login()
        games = self._scan()
        for game in games:
                print(game.text)
        # driver.find_element_by_link_text("Assassin's Creed: Director's Cut Edition").click()
        # driver.find_element_by_link_text("Enter to Win! (20P)").click()
        # driver.find_element_by_link_text("Dead Space").click()
        # driver.find_element_by_link_text("Enter to Win! (20P)").click()
        # driver.find_element_by_link_text("Logout").click()


if __name__ == "__main__":
    estimo = Estimo()
    if len(sys.argv) == 2 and sys.argv[1] == '-scan':
        estimo.scan()
        estimo.close()
