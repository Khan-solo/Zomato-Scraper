from bs4 import BeautifulSoup


import pandas as pd
import requests
import csv
import json
import datetime
import uuid

class DishScraper:
    def __init__(self, url, rest_id):
        """

        :param url: Url of the Restaurant's dine-out page on zomato
        :param rest_id: uuid of the restaurant
        """
        self.url = url
        self.rest_id = rest_id
        try:
            self.dish_data = pd.read_csv('data/Dish_Data.csv')
        except Exception as E:
            print(E)
            print("Dish Data File Not Found! Creating one.")
            self.dish_data = pd.DataFrame(columns=['Dish', 'Price', 'Type', 'Details', 'id', 'restaurant_id'])


    def clean_url(self):
        if "/info" in self.url:
            self.url = self.url.replace("/info", "/order")
            return "Url cleaned"

    def scrape_page(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"}
        print(self.clean_url()) #cleaning the url
        print("Url being scraped: ", self.url)
        response = requests.get(self.url, headers=headers) # Should use a proxy to prevent getting blocked
        soup = BeautifulSoup(response.text, "lxml")
        print(soup.title.text)
        self.soup = soup
        return "Page Scraped"

    def scrape_dishes_list(self):
        print("Scraping the list of dishes")
        dishes = self.soup.find_all('div', class_='sc-1s0saks-17 bGrnCu')
        for dish in dishes:
            try:
                type = dish.find('div', class_='sc-1tx3445-0 kcsImg sc-1s0saks-6 eEOGnT').get('type')
            except:
                type = ""
            try:
                name = dish.find('h4', class_='sc-1s0saks-15 iSmBPS').text
            except:
                name = ""
            try:
                price = dish.find('div', class_='sc-17hyc2s-3 jOoliK sc-1s0saks-8 gYkxGN').text.replace("₹", "")
            except:
                price = ""
            try:
                deets = dish.find('p', class_='sc-1s0saks-12 hcROsL').text
                if "... read more" in deets:
                    deets = ",".join(deets.split(",")[:-1]).strip() + " , + more"
            except:
                deets = ""
            self.dish_data.loc[len(self.dish_data)] = [name, price, type, deets, str(uuid.uuid4()), str(self.rest_id)]

    def run(self):
        print("Running The FLow")
        self.scrape_page()
        self.scrape_dishes_list()
        print("Dish Data Collected")
        self.dish_data = self.dish_data.drop_duplicates(subset=['Dish', 'restaurant_id'], keep='last')
        self.dish_data.to_csv("data/Dish_Data.csv", index=False)
        return "Successfully Scraped Dish Data"

if __name__ =="__main__":
    df = pd.read_csv("Lucknow_Restaurants.csv")
    url = df['Link'].values[20]
    Obj = DishScraper(url=url).run()
    print(Obj)