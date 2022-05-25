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
        path = "docs/Restaurants.html" #Hardcoded since the Html will be saved by this name
        restaurant_df = ZomatoDineoutRestuarants(city=self.city).scrape_rest_list(url=path, local=True)

        for i,r in restaurant_df.iterrows():
            try:
                url = r['Link']
                rest_id = r['id'] # to be made static
                Obj = DishScraper(url=url, rest_id=rest_id).run()
                # print(Obj)
            except Exception as E:
                print(E)
                print(r['Link'])
            print("="*30)

if __name__ == "__main__":
    cities = ['barabanki','Lucknow', 'ncr']
    for city in cities:
        Pipeline(city).run()
        print(f"Scraping Finished for {city}")
    print("Scraping Finished")
