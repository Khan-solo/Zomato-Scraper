import pandas as pd
import csv

from core.HtmlGenerator import RestaurantScraper
from core.RestaurantList import ZomatoDineoutRestuarants
from core.Dish_Scraper import DishScraper

class Pipeline:
    def __init__(self, city:str="Lucknow"):
        """
        :param city: City for which the scrapers need to run
        """
        self.city = city

    def run(self):
        print("Running Html Scraper")
        GenHtmlMsg = RestaurantScraper(city=self.city).run()
        print(GenHtmlMsg)
        path = "docs/Restaurants.html"
        Obj = ZomatoDineoutRestuarants(city=self.city).scrape_rest_list(url=path, local=True)


if __name__ == "__main__":
    Pipeline("Barabanki").run()
    print("Scraping Finished")
