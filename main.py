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
        ZomatoDineoutRestuarants(city=self.city).scrape_rest_list(url=path, local=True)
        restaurant_df = pd.read_csv("data/RestaurantsList.csv")
        for i,r in restaurant_df.head(5).iterrows():
            try:
                url = r['Link']
                rest_id = r['id']
                Obj = DishScraper(url=url, rest_id=rest_id).run()
                print(Obj)
            except Exception as E:
                print(E)
                print(r['Link'])
            # break

if __name__ == "__main__":
    Pipeline("Barabanki").run()
    print("Scraping Finished")
