from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

import pandas as pd
import json
import csv
import ast
import time

class RestaurantScraper:
    def __init__(self, city):
        self.city = city

    def get_page(self):
        url = "https://www.zomato.com/"+self.city.strip().lower()+"/dine-out"
        print(f"Url being scraped: {url}")

        s=Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.get(url=url)
        time.sleep(3)
        self.scroller()

    def scroller(self):
        print("Scrolling to the bottom")
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True
        print("Scrolling Complete")

    def write_page(self):
        print("Writing the HTML page to a file")
        with open("DineOutRestaurants.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
    def run(self):
        self.get_page()
        self.write_page()
        self.driver.quit()
        pass

if __name__ == "__main__":
    print("Running Zomato Scraper")
    city = input("Enter City Name: ")
    Obj = RestaurantScraper(city=city)
    Obj.run()
    print("Scraping Finished")










