# -*- coding: utf-8 -*-
from selenium import webdriver
import json


class Estimo:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.steamgifts.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        settings = json.load(open('settings.cfg'))
        self.username = settings['username']
        self.password = settings['password']

    def run(self):
        self.estimo()
        self.close()

    def close(self):
        self.driver.quit()

    def estimo(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("img.login").click()
        driver.find_element_by_id("steamAccountName").clear()
        driver.find_element_by_id("steamAccountName").send_keys(self.username)
        driver.find_element_by_id("steamPassword").clear()
        driver.find_element_by_id("steamPassword").send_keys(self.password)
        driver.find_element_by_id("imageLogin").click()
        games = driver.find_elements_by_class_name("title")
        for game in games:
            print(game.find_elements_by_tag_name("a")[0].text)
        # driver.find_element_by_link_text("Assassin's Creed: Director's Cut Edition").click()
        # driver.find_element_by_link_text("Enter to Win! (20P)").click()
        # driver.find_element_by_link_text("Dead Space").click()
        # driver.find_element_by_link_text("Enter to Win! (20P)").click()
        # driver.find_element_by_link_text("Logout").click()


if __name__ == "__main__":
    Estimo().run()
