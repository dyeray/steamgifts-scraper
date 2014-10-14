# -*- coding: utf-8 -*-

from settings import Settings
from selenium import webdriver
from pyvirtualdisplay import Display
import time


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

    def _scrape(self, deep=False):
        self.drv.get(self.base_url + "/")
        games = self.drv.find_elements_by_xpath(
            '//div[@class="ajax_gifts"]//div[@class="title"]//a')
        if deep:
            for i in range(2, 10):
                self.drv.get(self.page_url + i)
                games += self.drv.find_elements_by_xpath(
                    '//div[@class="ajax_gifts"]//div[@class="title"]//a')
        return games

    def scan(self, deep=False, dbg=False):
        self._start_driver(dbg)
        new_games = filter(lambda g: g not in self.settings.get_games(),
                           {g.text for g in self._scrape()})
        self._stop_driver()
        return new_games

    def subscribe(self, deep=False, debug=False):
        self._start_driver(debug)
        self._login()
        wanted_games = {k for k, v in self.settings.get_games().items() if v == 1}
        games = self._scrape()
        subscribed = []
        for game in games:
            if game.text not in wanted_games:
                continue
            game_title = game.text
            self.drv.execute_script("$(window.open('" + game.get_attribute("href") + "'))")
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
