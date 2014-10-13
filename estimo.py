# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
import json
import time
import argparse

SETTINGS_PATH = 'settings.cfg'


class Estimo:
    def __init__(self):
        self.base_url = "http://www.steamgifts.com"
        self.page_url = "http://www.steamgifts.com/open/page/"
        self.settings = self._load_settings()

    def _stop_driver(self):
        self.drv.quit()
        self.display.stop()

    def _start_driver(self, dbg=False):
        self.display = None
        if not dbg:
            display = Display(visible=0, size=(1280, 1014))
            display.start()
            self.display = display
        self.drv = webdriver.Firefox()
        self.drv.implicitly_wait(10)
        self.base_window = self.drv.current_window_handle

    def _login(self):
        self.drv.get(self.base_url + "/")
        self.drv.find_element_by_css_selector("img.login").click()
        self.drv.find_element_by_id("steamAccountName").clear()
        self.drv.find_element_by_id("steamAccountName").send_keys(self.settings['username'])
        self.drv.find_element_by_id("steamPassword").clear()
        self.drv.find_element_by_id("steamPassword").send_keys(self.settings['password'])
        self.drv.find_element_by_id("imageLogin").click()
        time.sleep(15)

    def _scan(self, deep=False):
        self.drv.get(self.base_url + "/")
        games = self.drv.find_elements_by_xpath(
            '//div[@class="ajax_gifts"]//div[@class="title"]//a')
        if deep:
            for i in range(2, 10):
                self.drv.get(self.page_url + i)
                games += self.drv.find_elements_by_xpath(
                    '//div[@class="ajax_gifts"]//div[@class="title"]//a')
        return games

    def _load_settings(self):
        return json.load(open(SETTINGS_PATH))

    def _save_settings(self):
        json.dump(self.settings, open(SETTINGS_PATH, "w"))

    def scan(self, deep=False, dbg=False):
        self._start_driver(dbg)
        games = self.settings["games"]
        new_games = {g.text for g in self._scan()}
        for ng in new_games:
            if ng not in games:
                decision = raw_input("New game found: '" + ng + "'. Do you want to automatically" +
                                     " access its giveaways (y/n/q)?")
                if decision == 'y':
                    self.settings["games"][ng] = 1
                elif decision == 'n':
                    self.settings["games"][ng] = 0
                else:
                    break
        self._save_settings()
        self._stop_driver()

    def subscribe(self, deep=False, debug=False):
        self._start_driver(debug)
        self._login()
        wanted_games = {k for k, v in self.settings["games"].items() if v == 1}
        games = self._scan()
        for game in games:
            if game.text in wanted_games:
                print(game.text)
                self.drv.execute_script("$(window.open('" + game.get_attribute("href") + "'))")
                self.drv.switch_to_window(self.drv.window_handles[-1])
                try:
                    self.drv.find_element_by_partial_link_text("Enter to Win").click()
                except NoSuchElementException:
                    pass
                self.drv.close()
                self.drv.switch_to_window(self.base_window)
        self._stop_driver()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='steamgifts.com client')
    parser.add_argument('-s', '--scan', const='scan', default='play', nargs='?', dest='operation',
                        help='Scan the webpage and choose what games you want')
    parser.add_argument('-f', '--full', const=True, default=False, nargs='?',
                        help='Work on all pages, not just on the first one (frontpage - page 1)')
    parser.add_argument('-d', '--debug', const=True, default=False, nargs='?',
                        help='Show the browser window')
    estimo = Estimo()
    argss = parser.parse_args()
    if argss.operation == 'scan':
        estimo.scan(argss.full, argss.debug)
    else:
        estimo.subscribe(argss.full, argss.debug)
