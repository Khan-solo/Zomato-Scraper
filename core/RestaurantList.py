"""
Author: Mursil Khan
"""
from bs4 import BeautifulSoup
import pandas as pd
import uuid

class ZomatoDineoutRestuarants:
    def __init__(self, city):
        self.city = city
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

                #Tags-------------
                try:
                    tags = restaurant.find('p', class_='iumJIm').text.strip()
                except:
                    tags = ""

                #Price-----------
                try:
                    price = restaurant.find('p', class_='fXNJYh').text.replace("₹", "").strip()
                except:
                    price = ""

                #Location--------
                try:
                    location = restaurant.find('p', class_='iJapJD').text.strip().split(",")
                # print(location)
                    city = location[-1].strip()
                    area = ",".join(location[:-1]).strip()
                except:
                    area = ""
                    city = self.city.title()
                #Link-------------
                link = restaurant.find('a', class_='sc-gleUXh')['href']
                if "www" not in link:
                    link = "https://www.zomato.com"+link

                #Rating-----------
                try:
                    rating = restaurant.find('div', class_='cILgox').text.strip()
                except:
                    rating = "-"
                # cols = ['id', 'Name', 'Tags', 'Price', 'Area', 'City', 'Link']
                df.loc[index] = [str(uuid.uuid4()), name, tags, price, area, city, rating, link]
        df.to_csv("data/RestaurantsList.csv", index=False)
        return "Data Stored"

if __name__=="__main__":
    Obj = Zomato()
    url = r"C:\Users\Mursil\Desktop\ZomatoProject\Dine-Out Restaurants in Lucknow - Zomato.html"
    msg = Obj.scrape_rest_list(url)
    print(msg)