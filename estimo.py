# -*- coding: utf-8 -*-

from settings import Settings
from selenium import webdriver
from pyvirtualdisplay import Display
import time


class Game:
    def __init__(self, title, href):
        self.title = title
        self.href = href


class Estimo:
    def __init__(self):
        self.base_url = "http://www.steamgifts.com"
        self.page_url = "http://www.steamgifts.com/open/page/"
        self.settings = Settings()

    def _stop_driver(self):
        self.drv.quit()
        if self.display:
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
        self.drv.find_element_by_id("steamAccountName").send_keys(self.settings.get_username())
        self.drv.find_element_by_id("steamPassword").clear()
        self.drv.find_element_by_id("steamPassword").send_keys(self.settings.get_password())
        self.drv.find_element_by_id("imageLogin").click()
        time.sleep(15)

    def _build_games_list(self, games):
        # Extract the game information we want from the selenium nodes
        games_list = []
        for game in games:
            games_list.append(Game(game.text, game.get_attribute("href")))
        return games_list

    def _scrape(self, full=False):
        self.drv.get(self.base_url + "/")
        games = self._build_games_list(self.drv.find_elements_by_xpath(
            '//div[@class="ajax_gifts"]//div[@class="title"]//a'))
        if full:
            for i in range(2, 10):
                self.drv.get(self.page_url + str(i))
                games += self._build_games_list(self.drv.find_elements_by_xpath(
                    '//div[@class="ajax_gifts"]//div[@class="title"]//a'))
        return games

    def scan(self, full=False, dbg=False):
        self._start_driver(dbg)
        new_games = filter(lambda g: g not in self.settings.get_games(),
                           {g.title for g in self._scrape(full)})
        self._stop_driver()
        return new_games

    def subscribe(self, full=False, debug=False):
        self._start_driver(debug)
        self._login()
        wanted_games = {k for k, v in self.settings.get_games().items() if v == 1}
        games = self._scrape(full)
        subscribed = []
        for game in games:
            if game.title not in wanted_games:
                continue
            game_title = game.title
            self.drv.execute_script("$(window.open('" + game.href + "'))")
            self.drv.switch_to_window(self.drv.window_handles[-1])
            giveaway = self.drv.find_elements_by_xpath(
                '//form[@id="form_enter_giveaway"]//a')[0]
            if giveaway.text.startswith('Enter to Win'):
                self.drv.find_element_by_partial_link_text("Enter to Win").click()
                subscribed.append(game_title)
            self.drv.close()
            self.drv.switch_to_window(self.base_window)
        self._stop_driver()
        return subscribed
