"""
Author: Mursil Khan
"""
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
import csv
import uuid

class Zomato:
    def __init__(self):

        pass

    def scrape_rest_list(self, url, local=True):
        """
        :param url: Url of homepage (dine-out page) of a city.
        :param local: True if a local HTML file is being read. False if the web_page
                    needs to be scraped*
        :return: Pandas Dataframe with restaurant details
        """
        if local:
            with open(url, encoding="utf8") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
        print(soup.title.text)
        columns = ['id', 'Name', 'Tags', 'Price', 'Area', 'City', 'Rating', 'Link']
        df = pd.DataFrame(columns=columns)
        # Finding restaurants----------
        rows = soup.find_all('div', class_="sc-1mo3ldo-0")
        for row in rows:
            restaurants = row.find_all('div', class_='sc-jhaWeW')
            for restaurant in restaurants:
                index = len(df)

                #Name-------------
                name = restaurant.find('h4', class_='sc-1hp8d8a-0').text.strip()
                print(name)

                #Tags-------------
                tags = restaurant.find('p', class_='iumJIm').text.strip()
                print(tags)

                #Price-----------
                price = restaurant.find('p', class_='fXNJYh').text.replace("₹", "").strip()
                print(price)

                #Location--------
                location = restaurant.find('p', class_='iJapJD').text.strip().split(",")
                # print(location)
                city = location[-1].strip()
                area = ",".join(location[:-1]).strip()
                print(area)
                print(city)
                #Link-------------
                link = restaurant.find('a', class_='sc-gleUXh')['href']
                print(link)

                #Rating-----------
                rating = restaurant.find('div', class_='cILgox').text.strip()
                print(rating)
                # cols = ['id', 'Name', 'Tags', 'Price', 'Area', 'City', 'Link']
                df.loc[index] = [str(uuid.uuid4()), name, tags, price, area, city, rating, link]
                print("="*30)
        return df

if __name__=="__main__":
    Obj = Zomato()
    url = r"C:\Users\Mursil\Desktop\ZomatoProject\Dine-Out Restaurants in Lucknow - Zomato.html"
    data = Obj.scrape_rest_list(url)
    data.to_csv("Lucknow_Restaurants.csv", index=False)